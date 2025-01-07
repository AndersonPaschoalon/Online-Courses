from random import randint
from faker import Faker


class DummyRecipes:

    @staticmethod
    def rand_ratio():
        return randint(840, 900), randint(473, 573)
    
    def __init__(self):
        self.fake = Faker('pt_BR')


    def make_recipe(self):
        return {
            'id': self.fake.random_number(digits=2, fix_len=True),
            'title': self.fake.sentence(nb_words=6),
            'description': self.fake.sentence(nb_words=12),
            'preparation_time': self.fake.random_number(digits=2, fix_len=True),
            'preparation_time_unit': 'Minutos',
            'servings': self.fake.random_number(digits=2, fix_len=True),
            'servings_unit': 'Porção',
            'preparation_steps': self.fake.text(3000),
            'created_at': self.fake.date_time(),
            'author': {
                'first_name': self.fake.first_name(),
                'last_name': self.fake.last_name(),
            },
            'category': {
                'name': self.fake.word()
            },
            'cover': {
                # 'url': 'https://loremflickr.com/%s/%s/food,cook' % DummyRecipes.rand_ratio(),
                'url': 'https://picsum.photos/seed/{0}/800/450'.format(randint(0, 999)),
            }
        }


if __name__ == '__main__':
    from pprint import pprint
    pprint(DummyRecipes().make_recipe())

