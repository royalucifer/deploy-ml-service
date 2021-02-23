import re
from typing import List
from subprocess import check_call

import numpy as np
import nmslib
from annoy import AnnoyIndex

FILE_PATTERN = re.compile('(?P<uri>[a-zA-Z][-a-zA-Z0-9+.]*)://.*/(?P<file>.*)$')


def move_files(source: str, destination: str):
    check_call(['gsutil', '-m', 'cp', '-r', source, destination])


class AnnBase:
    def __init__(self, data: List[np.ndarray] = None, mapping: List[str] = None):
        self.data = data
        self.mapping = mapping

    def build_index(self):
        raise NotImplementedError

    def search_vec_top_n(self, vector, n: int):
        raise NotImplementedError

    def _save_file(self, path: str):
        raise NotImplementedError

    def _load_file(self, path: str, **kwargs):
        raise NotImplementedError

    def load(self, path: str, **kwargs):
        match_result = FILE_PATTERN.match(path.strip())
        if match_result is None:
            self._load_file(path)
        else:
            uri = match_result.groupdict()['uri']
            file = match_result.groupdict()['file']
            if uri == 'gs':
                move_files(path, file)
                self._load_file(file, **kwargs)

    def save(self, path: str):
        match_result = FILE_PATTERN.match(path.strip())
        if match_result is None:
            self._save_file(path)
        else:
            uri = match_result.groupdict()['uri']
            file = match_result.groupdict()['file']
            if uri == 'gs':
                self._save_file(file)
                move_files(file, path)


class Annoy(AnnBase):
    def __init__(self, vector_len: int,
                 metric: str = 'angular', **kwargs):
        super().__init__(**kwargs)
        self.index = AnnoyIndex(vector_len, metric=metric)

    def build_index(self, num_trees: int = 30):
        for i, embed in enumerate(self.data):
            self.index.add_item(i, embed)
        self.index.build(num_trees)

    def search_vec_top_n(self, vector, n: int = 5):
        neighbours = self.index.get_nns_by_vector(vector, n)
        result = []
        for idx in neighbours:
            result.append(self.mapping[idx])
        return result

    def _load_file(self, path: str, **kwargs):
        self.index.load(path)

    def _save_file(self, path: str):
        self.index.save(path)


class NMSLib(AnnBase):
    def __init__(self, method: str = 'hnsw',
                 metric: str = 'cosinesimil', **kwargs):
        super().__init__(**kwargs)
        self.index = nmslib.init(method=method, space=metric)

    def build_index(self, m: int = 20, ef: int = 300, post: int = 2):
        data = np.vstack(self.data)
        self.index.addDataPointBatch(data)
        index_params = {
            'M': m,
            'efConstruction': ef,
            'post': post}
        self.index.createIndex(index_params)

    def search_vec_top_n(self, vector, n: int = 5):
        neighbours, distance = self.index.knnQuery(vector, k=n)
        items = []
        for idx in neighbours:
            items.append(self.mapping[idx])
        return items, distance.tolist()

    def _load_file(self, path: str, ef: int = None):
        self.index.loadIndex(path)
        if ef is not None:
            self.index.setQueryTimeParams({'efSearch': ef})

    def _save_file(self, path: str):
        self.index.saveIndex(path)
