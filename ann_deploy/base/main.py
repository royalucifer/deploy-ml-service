import os
import pickle

from flask import Flask, jsonify, request

from ann_search import NMSLib

# Parameters
METRIC = 'cosinesimil'
BASE_DIR = '/opt/workdir/AnnSearch'
INDEX_DIR = os.path.join(BASE_DIR, 'embedding.ann')
MAPPING_DIR = os.path.join(BASE_DIR, 'mapping.pkl')

# Initialize ANN
with open(MAPPING_DIR, 'rb') as f:
    mapping = pickle.load(f)
ann_util = NMSLib(method='hnsw', metric=METRIC, mapping=mapping)
ann_util.load(INDEX_DIR)

# Initialize Flask app
app = Flask(__name__)


@app.route('/get_similarity', methods=['POST'])
def get_similarity():
    """
    Given a vector, return a list of recommended item ids.
    ---
    Parameters:
        vector: document vector.
        num_recs: The number of news id should be recommended.
    """
    vector = request.form.get('vector')
    num_recs = request.form.get('num_recs')

    try:
        vector = [float(v) for v in vector.split(',')]
    except:
        return 'No vector provided.', 400

    try:
        num_recs = int(num_recs)
    except:
        return 'User id and number of recs arguments must be integers.', 400

    try:
        items, distances = ann_util.search_vec_top_n(vector, num_recs)
    except:
        return 'Can not found similar document', 400

    json_response = jsonify({'pid': items, 'distance': distances})
    return json_response, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)), debug=True)
