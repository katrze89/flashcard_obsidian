import json

# def parse_output_to_json(raw_output: str) -> list:
#     """
#     Funkcja przyjmuje raw_output (string) i zwraca listę słowników (obiektów JSON).
#     Zakłada, że raw_output to JSON, który po sparsowaniu daje listę z jednym elementem - stringiem.
#     Ten string zawiera kilka obiektów JSON oddzielonych przecinkami.
#     """
#     try:
#         # Najpierw parsujemy raw_output jako JSON
#         parsed = json.loads(raw_output)
#     except json.JSONDecodeError as e:
#         raise ValueError(f"Invalid JSON input: {e}")

#     # Jeśli parsowany wynik to lista zawierająca jeden element typu string
#     if isinstance(parsed, list) and len(parsed) == 1 and isinstance(parsed[0], str):
#         inner_str = parsed[0]

#         # Spróbujemy opakować ten string w nawiasy kwadratowe, by uzyskać poprawny JSON array
#         candidate = f'[{inner_str}]'
#         try:
#             result = json.loads(candidate)
#             return result
#         except json.JSONDecodeError:
#             # Jeśli powyższa próba się nie powiedzie, spróbujemy wyekstrahować pojedyncze obiekty za pomocą regex.
#             objects = re.findall(r'\{.*?\}', inner_str, re.DOTALL)
#             result = []
#             for obj_str in objects:
#                 try:
#                     obj = json.loads(obj_str)
#                     result.append(obj)
#                 except json.JSONDecodeError:
#                     continue
#             return result
#     elif isinstance(parsed, list) or isinstance(parsed, dict):
#         # Jeśli parsed to już lista obiektów, zwracamy ją
#         return parsed
#     else:
#         raise ValueError("Input JSON is not in an expected format.")


def parse_output_to_json(raw_output: str) -> dict[str, str] | list[dict[str, str]]:
    if raw_output.startswith("```json"):
        raw_output = raw_output[8:]

    if raw_output.endswith("```"):
        raw_output = raw_output[:-3]

    try:
        result: dict[str, str] | list[dict[str, str]] = json.loads(raw_output)
        return result
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON input: {e}")
