import pickle

try:
    with open('models/basic_model.pkl', 'rb') as f:
        data = pickle.load(f)
    print('✓ Successfully loaded model')
    print(f'Type: {type(data)}')
    if isinstance(data, dict):
        print(f'Keys: {list(data.keys())}')
except Exception as e:
    print(f'✗ Error loading model: {type(e).__name__} - {e}')
