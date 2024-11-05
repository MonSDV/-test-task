import json
import sys
import itertools

def generate_versions(template):
    """Генерирует две версии из шаблона, заменяя '*' на числа"""
    parts = template.split('.')
    asterisks_indices = [i for i, part in enumerate(parts) if part == '*']
    versions = []

    # Комбинации для замен *
    replacements_list = [
        [1] * len(asterisks_indices),
        [2] * len(asterisks_indices)
    ]

    for replacements in replacements_list:
        version_parts = parts.copy()
        for idx, replacement in zip(asterisks_indices, replacements):
            version_parts[idx] = str(replacement)
        versions.append('.'.join(version_parts))

    return versions

def compare_versions(version1, version2):
    """Сравнивает две строковые версии"""
    v1_parts = list(map(int, version1.split('.')))
    v2_parts = list(map(int, version2.split('.')))

    # Выравниваем версии по длине, заполняя нулями
    max_length = max(len(v1_parts), len(v2_parts))
    v1_parts.extend([0] * (max_length - len(v1_parts)))
    v2_parts.extend([0] * (max_length - len(v2_parts)))

    for part1, part2 in zip(v1_parts, v2_parts):
        if part1 != part2:
            return part1 < part2
    return False

def main(version_input, config_file):
    with open(config_file, 'r') as file:
        templates = json.load(file)

    # Генерация версий на основе шаблона
    all_versions = []
    for key, template in templates.items():
        versions = generate_versions(template)
        all_versions.extend(versions)
        print(f"Generated versions for {key}: {versions}")

    # Удаление дублей и сортировка версий
    all_versions = sorted(set(all_versions), key=lambda v: [int(part) for part in v.split('.')])

    # Печать отсортированных версий
    print("\nAll Versions:")
    for version in all_versions:
        print(version)

    # Фильтруем и печатаем версии, более старые, чем входная версия
    older_versions = [v for v in all_versions if compare_versions(v, version_input)]
    print(f"\nVersions older than {version_input}:")
    for version in older_versions:
        print(version)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 02_templates.py <version> <config_file>")
        sys.exit(1)

    version_input = sys.argv[1]
    config_file = sys.argv[2]
    main(version_input, config_file)
