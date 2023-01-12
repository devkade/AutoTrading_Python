def get_key(exchange):
    with open(f'./{exchange}.txt') as f:
        lines = f.readlines()
        api_key = lines[0].strip()
        api_secret = lines[1].strip()

    return api_key, api_secret
