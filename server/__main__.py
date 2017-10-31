from os import path

import eve


def main():
    app = eve.Eve(settings=path.join(path.dirname(path.realpath(__file__)), 'settings.py'))
    app.run()


if __name__ == '__main__':
    main()
