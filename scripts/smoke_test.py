from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

errors = []

def try_post(path, payload):
    r = client.post(path, json=payload)
    print(f"POST {path} -> {r.status_code}")
    try:
        print(r.json())
    except Exception:
        print(r.text)
    if r.status_code not in (200, 201):
        errors.append((path, r.status_code, r.text))

if __name__ == '__main__':
    try_post('/media/', {'alt_text': 'Sample image', 'extension': 'jpg', 'url': 'http://example.com/image.jpg'})
    try_post('/images/', {'alt_text': 'A cat', 'extension': 'png', 'url': 'http://example.com/cat.png'})
    try_post('/videos/', {'alt_text': 'A dog video', 'extension': 'mp4', 'url': 'http://example.com/dog.mp4'})
    r = client.get('/media/')
    print(f"GET /media/ -> {r.status_code}")
    try:
        print(r.json())
    except Exception:
        print(r.text)

    if errors:
        print('\nSMOKE TEST: FAILED')
        for e in errors:
            print(e)
        raise SystemExit(1)
    else:
        print('\nSMOKE TEST: PASSED')
        raise SystemExit(0)

