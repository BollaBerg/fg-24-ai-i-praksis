from pathlib import Path
import json
import csv


def get_all_messages(directory: Path):
    parsed = []
    for message_file in directory.iterdir():
        if not message_file.is_file():
            continue
        with message_file.open('r') as f:
            decoded = json.load(f)
            message: dict
            for message in decoded:
                text: str = message.get('text')
                if text is None or 'the channel' in text:
                    continue
                ts: str = message.get('ts')
                parsed.append((text.replace('\n', ' '), ts))
    return parsed


def get_top_level_messages(directory: Path):
    parsed = []
    for message_file in directory.iterdir():
        if not message_file.is_file():
            continue
        with message_file.open('r') as f:
            decoded = json.load(f)
            message: dict
            for message in decoded:
                if message.get('reply_count', None) is None:
                    continue
                text: str = message.get('text')
                if text is None or 'the channel' in text or text == '':
                    continue
                ts: str = message.get('ts')
                parsed.append((text.replace('\n', ' '), ts))
    return parsed


def get_messages_from_data_dir(directory: Path):
    messages = []
    for subdir in directory.iterdir():
        if not subdir.is_dir():
            continue
        messages.extend(get_all_messages(subdir))
    return messages


def get_top_level_messages_from_data_dir(directory: Path):
    messages = []
    for subdir in directory.iterdir():
        if not subdir.is_dir():
            continue
        messages.extend(get_top_level_messages(subdir))
    return messages


def write_to_file(data: list[tuple[str, str]], outfile: Path):
    with outfile.open('w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='|')
        writer.writerow(['message', 'ts'])
        writer.writerows(data)


if __name__ == "__main__":
    data_path = Path().absolute().parent / 'data'
    processed_path = data_path / 'processed'
    processed_path.mkdir(parents=True, exist_ok=True)

    for timespan in ['month', '2023']:
        # Spørrekroken
        dir_path = data_path / f'raw_{timespan}' / 'spørrekroken'
        all_messages_sk = get_all_messages(dir_path)
        write_to_file(all_messages_sk, processed_path / f'spørrekroken_all_{timespan}.txt')

        top_level_messages_sk = get_top_level_messages(dir_path)
        write_to_file(top_level_messages_sk, processed_path / f'spørrekroken_top_{timespan}.txt')

        # All
        all_messages = get_messages_from_data_dir(data_path / f'raw_{timespan}')
        write_to_file(all_messages, processed_path / f'all_{timespan}.txt')

        top_level_messages = get_top_level_messages_from_data_dir(data_path / f'raw_{timespan}')
        write_to_file(top_level_messages, processed_path / f'all_top_{timespan}.txt')

    print(f"Files written to {processed_path.absolute()}")
