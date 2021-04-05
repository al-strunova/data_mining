from pathlib import Path
import json
import time
import requests


class Category:
    def __init__(self, name, code, products):
        self.name = name
        self.code = code
        self.products = products

    def __str__(self):
        return str(self.__dict__)


class Parse5ka:
    headers = {"User-Agent": "Phillip Kirkorov"}

    def __init__(self, base_url: str, save_path: Path):
        self.base_url = base_url
        self.save_path = save_path

    def _get_response(self, url, *args, **kwargs) -> requests.Response:
        while True:
            response = requests.get(url, *args, **kwargs)
            if response.status_code == 200:
                return response
            time.sleep(1)

    def run(self):
        response = self._get_response(self.base_url + "/categories/")
        data: dict = response.json()
        for category in data:
            category_obj = Category(
                category["parent_group_name"],
                category["parent_group_code"],
                self._get_products(category["parent_group_code"]),
            )
            print(category_obj.__str__())
            category_path = self.save_path.joinpath(f"{category_obj.code}.json")
            self._save(category_obj, category_path)

    def _save(self, data, file_path):
        file_path.write_text(json.dumps(str(data), ensure_ascii=False))

    def _get_products(self, code):
        response = self._get_response(self.base_url + f"/special_offers/?categories={code}")
        data: dict = response.json()
        products = data["results"]
        return products


def get_save_path(dir_name):
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path


parser = Parse5ka("https://5ka.ru/api/v2", get_save_path("categories"))
parser.run()
