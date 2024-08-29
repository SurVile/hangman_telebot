def historical_truth(*events, name="Rocinante", **choice):
    definitions = set()
    for event in events:
        common_letters = sum(1 for char in event.lower() if char in name.lower())
        if 'letters' in choice:
            if common_letters >= choice['letters']:
                if 'length' in choice:
                    if len(event) + len(name) <= choice['length']:
                        definitions.add(event)
                else:
                    definitions.add(event)
        elif 'length' in choice:
            if len(event) + len(name) <= choice['length']:
                definitions.add(event)
        else:
            definitions.add(event)

    sorted(definitions)
    return definitions


def main():
    events = ["long", "skinny", "bony", "exhausted", "sunken"]
    choice = {
        "letters": 2,
        "length": 15
    }
    print(*historical_truth(*events, **choice), sep="\n")


if __name__ == '__main__':
    main()
