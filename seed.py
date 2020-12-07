from app import app
from models import db, User, Post, Tag, PostTag

db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()

#---------| Add Users |---------#
first_names = ('Joe', 'Sellers', 'James', 'Poké',
               'Emma', 'Ruth Bader', 'Yang', 'Kurt')
last_names = ('Orlowski', 'Crisp', 'Peachy', 'Mon',
              'Watson', 'Ginsburg', 'Gang', 'Cobain')
image_urls = (
    'https://twirpz.files.wordpress.com/2015/06/twitter-avi-gender-balanced-figure.png',
    'https://impact-psy.com/desempeno/assets/images/avatars/profile-pic.jpg',
    'https://twirpz.files.wordpress.com/2015/06/twitter-avi-gender-balanced-figure.png',
    'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/07276519-74b6-4f25-b621-735a90607dd5/d3cp8rs-d091eb8f-96ca-4d86-b91b-cf5893f9f033.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvMDcyNzY1MTktNzRiNi00ZjI1LWI2MjEtNzM1YTkwNjA3ZGQ1XC9kM2NwOHJzLWQwOTFlYjhmLTk2Y2EtNGQ4Ni1iOTFiLWNmNTg5M2Y5ZjAzMy5naWYifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ._P6dOgXvKa-h13V7VbTPTi8uUm3NnH_tqk85ssBYb7I',
    'https://media0.giphy.com/media/yFBvng6mJMrDi/giphy.gif',
    'https://media1.tenor.com/images/5e31cef90f0465deca91115fb5b8caa6/tenor.gif?itemid=8883260',
    'https://media0.giphy.com/media/US6bb5xRxSZ1u4Qve2/giphy.gif',
    'https://media4.giphy.com/media/3oriO6yTZKmTqUI9tS/200.gif'
)

users = [User(first_name=user[0], last_name=user[1], image_url=user[2])
         for user in zip(first_names, last_names, image_urls)]

db.session.add_all(users)
db.session.commit()

#---------| Add Posts |---------#
titles = ('I am Awesome', 'You are Awesome', 'This is Awesome',
          'We are Awesome', 'They are Awesome', 'She is Awesome',
          'He is Awesome', 'Thou art Awesome')
bodies = (
    'Nulla in dolor at odio laoreet ultrices et at mauris.',
    'Donec pellentesque risus non nibh venenatis iaculis.',
    'Mauris laoreet est at justo imperdiet, eget vehicula ex aliquam.',
    'Nam sit amet nisi et elit sodales convallis.',
    'Vestibulum vel nisl lobortis, blandit tortor at, porta ex.',
    'Curabitur accumsan justo quis arcu ullamcorper, at tempus augue ultricies.',
    'Suspendisse efficitur orci sit amet nibh suscipit elementum.',
    'Donec eleifend eros ut urna viverra, ut consectetur odio semper.'
)
user_ids = (1, 1, 4, 2, 8, 8, 8)
post = zip(titles, bodies, user_ids)
posts = [Post(title=post[0], body=post[1], user_id=post[2]) for post in post]

db.session.add_all(posts)
db.session.commit()

#---------| Add Tags |---------#
tag_names = ('love', 'awesome', 'tech', 'python',
             'flask', 'postgresql', 'sqlalchemy')
tags = [Tag(name=name) for name in tag_names]

db.session.add_all(tags)
db.session.commit()

post_tags_ids = ((1, 1), (2, 1), (2, 2), (3, 4), (4, 4), (4, 5), (5, 3),
                 (5, 1), (6, 3), (7, 5), (7, 7), (1, 7), (1, 2), (1, 3),
                 (1, 4), (1, 5), (1, 6))
post_tags = [PostTag(post_id=post_tags_ids[0], tag_id=post_tags_ids[1])
             for post_tags_ids in post_tags_ids]

db.session.add_all(post_tags)
db.session.commit()
