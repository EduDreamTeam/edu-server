from distutils.core import setup

setup(name='edu-server',
      version='0.0.1',
      description='Education project server',
      author='EduDreamTeam',
      url='https://github.com/EduDreamTeam/edu-server',
      requires=['flask', 'flask_jwt', 'SQLAlchemy']
      )
