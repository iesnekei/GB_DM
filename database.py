from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hw_3_2
from sqlalchemy.exc import  IntegrityError, InvalidRequestError

engine = create_engine('sqlite:///gb_blog.db')

hw_3_2.Base.metadata.create_all(bind=engine)

SessionMaker = sessionmaker(bind=engine)

if __name__ == '__main__':
    db = SessionMaker()
    hw_3 = hw_3_2.GB(' https://geekbrains.ru/posts/')
    hw_3.get_soup(' https://geekbrains.ru/posts/')
    hw_3.get_post()
    hw_3.get_info()
    for i in range(0, len(hw_3.post_list)):
        users_check = []
        tags_check = []

        if hw_3.post_list[i]['user_id'] not in users_check:
            user = hw_3_2.Users(
                id=hw_3.post_list[i]['user_id'],
                url=f" 'https://geekbrains.ru//users/{hw_3.post_list[i]['url']}",
                name=hw_3.post_list[i]['user']
            )
            users_check.append(hw_3.post_list[i]['user_id'])

        post = hw_3_2.Post(
            url=hw_3.post_list[i]['url'],
            img_url=str(hw_3.post_list[i]['first_img']),
            data=hw_3.post_list[i]['post_date'],
            title=hw_3.post_list[i]['title'],
            author_id = user.id
        )

        for j in hw_3.post_list[i]['tags']:
            if j not in tags_check:
                tags_check.append(j)
                tag = hw_3_2.Tags(
                    name=j
                )

            tap = hw_3_2.Tag_and_post(
                post_id=post.id,
                tag_id=tag.id
            )
            print(1)
            try:
                db.add(tap)
                db.commit()
            except IntegrityError or InvalidRequestError:
                print(1)
                continue



    db.close()

    print(1)
