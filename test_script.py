import datetime
import json
import time
from datetime import datetime as dt

import requests


class UserPostData:
    USER_1_POST_ID = None
    USER_1_ID = None

    USER_2_POST_ID = None
    USER_2_ID = None

    USER_3_POST_ID = None
    USER_3_ID = None

    USER_4_POST_ID = None
    USER_4_ID = None

    def set_user_1_post_id(self, pk):
        self.USER_1_POST_ID = pk

    def set_user_1_id(self, pk):
        self.USER_1_ID = pk

    def set_user_2_post_id(self, pk):
        self.USER_2_POST_ID = pk

    def set_user_2_id(self, pk):
        self.USER_2_ID = pk

    def set_user_3_post_id(self, pk):
        self.USER_3_POST_ID = pk

    def set_user_3_id(self, pk):
        self.USER_3_ID = pk

    def set_user_4_post_id(self, pk):
        self.USER_4_POST_ID = pk

    def set_user_4_id(self, pk):
        self.USER_4_ID = pk


pizza_data = UserPostData()


def test_case_runner(ip, test_cases):
    """
    We call a series of functions that each demonstrate a specific functionality. We dont make
    and assertions in the code as this could potential cause the programme to  terminate
    unexpectedly (assertions about API responses can be seen in the numerous test cases) rather
    we call on the user to enter "y" to cycle through the 20 different test cases and check the
    output themselves.

    NOTE: You can set the IP address in the `if __name__ == "__main__" block.
    """

    print(
        "\nThis app cycles through 20 test cases that demonstrate the Pizza API functionality.\n"
    )

    user_1 = input(
        "Enter (female) user name 1 or carriage return for default user 'Olga': "
    )
    if not user_1:
        user_1 = "Olga"
    user_2 = input(
        "Enter (male) user name 2 or carriage return for default user 'Nick': "
    )
    if not user_2:
        user_2 = "Nick"
    user_3 = input(
        "Enter (female) user name 3 or carriage return for default user 'Mary': "
    )
    if not user_3:
        user_3 = "Mary"
    user_4 = input(
        "Enter (male) user name 4 or carriage return for default user 'Nestor': "
    )
    if not user_4:
        user_4 = "Nestor"

    for idx, test in enumerate(test_cases):
        print(f"\n---- test case: {idx + 1} ----")
        test(ip, user_1, user_2, user_3, user_4)


def tc1(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_1}, {user_2}, {user_3} and {user_4} register and are ready to access "
        f"the Pizza API.\n"
    )

    def create_users():
        for user in [user_1, user_2, user_3, user_4]:
            requests.post(
                url=f"{ip}create-user",
                json={"username": user, "password": "password123"},
            )
            response = requests.get(url=f"{ip}users/{user}")
            print(
                f"Status code when retrieving details for {user}: {response.status_code}"
            )

    create_users()

    get_user_1 = requests.get(url=f"{ip}users/{user_1}")
    user_1_id = json.loads(get_user_1.content)["id"]
    pizza_data.set_user_1_id(user_1_id)

    get_user_2 = requests.get(url=f"{ip}users/{user_2}")
    user_2_id = json.loads(get_user_2.content)["id"]
    pizza_data.set_user_2_id(user_2_id)

    get_user_3 = requests.get(url=f"{ip}users/{user_3}")
    user_3_id = json.loads(get_user_3.content)["id"]
    pizza_data.set_user_3_id(user_3_id)

    get_user_4 = requests.get(url=f"{ip}users/{user_4}")
    user_4_id = json.loads(get_user_4.content)["id"]
    pizza_data.set_user_4_id(user_4_id)


def tc2(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_1}, {user_2}, {user_3} and {user_4} use the oAuth v2 authorisation "
        f"service to register and get their tokens.\n"
    )

    print("SKIPPED")


def tc3(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_1} makes a call to the API without using her token. This call should "
        f"be unsuccessful as the user is unauthorised.\n"
    )

    print("SKIPPED")


def tc4(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_1} posts a message in the Tech topic with an expiration time of now."
        f" After the end of the expiration time, the message will not accept any further user "
        f"interactions.\n"
    )

    # user_1 creates a post
    data = {
        "expires_at": f"{dt.now()}",
        "author": pizza_data.USER_1_ID,
        "title": "Post 1",
        "body": "A really long post body",
        "topics": ["Tech"],
    }
    create_post = requests.post(url=f"{ip}create-post", json=data)
    post_id = json.loads(create_post.content)["id"]
    pizza_data.set_user_1_post_id(post_id)

    # user_2 post a reaction against user_1's post
    reaction = {
        "like_or_dislike": "Like",
        "comment": "I really like this post",
        "author": pizza_data.USER_2_ID,
        "post": post_id,
    }
    reaction = requests.post(url=f"{ip}add-reaction", json=reaction)

    print(
        "The post to 'add-reaction' should return a 400 as the post is no longer accepting "
        "request"
    )
    print(f"Status code of post to 'add-reaction': {reaction.status_code}")
    print(
        f"Returned message of post to 'add-reaction': "
        f"{json.loads(reaction.content)['non_field_errors'][0]}"
    )


def tc5(ip, user_1, user_2, user_3, user_4):
    # todo: need to add authentication
    print(
        f"TEST CASE: {user_2} posts a message in the Tech topic with an expiration time using his "
        "token.\n"
    )

    data = {
        "expires_at": f"{dt.now() + datetime.timedelta(days=10)}",
        "author": pizza_data.USER_2_ID,
        "title": "Post 2",
        "body": "A really long post body",
        "topics": ["Tech"],
    }
    post = requests.post(url=f"{ip}create-post", json=data)
    post_id = json.loads(post.content)["id"]
    pizza_data.set_user_2_post_id(post_id)
    print(f"Status code of post: {post.status_code}")
    print(json.loads(post.content))


def tc6(ip, user_1, user_2, user_3, user_4):
    # todo: need to add authentication
    print(
        f"TEST CASE: {user_3} posts a message in the Tech topic with an expiration time using her "
        "token.\n"
    )

    data = {
        "expires_at": f"{dt.now() + datetime.timedelta(days=10)}",
        "author": pizza_data.USER_3_ID,
        "title": "Post 3",
        "body": "A really long post body",
        "topics": ["Tech"],
    }
    post = requests.post(url=f"{ip}create-post", json=data)
    post_id = json.loads(post.content)["id"]
    pizza_data.set_user_3_post_id(post_id)
    print(f"Status code of post: {post.status_code}")
    print(json.loads(post.content))


def tc7(ip, user_1, user_2, user_3, user_4):
    # todo: need to add authentication
    print(
        f"TEST CASE: {user_2} browses all the available posts in the Tech topic, there should be "
        f"three posts available with zero likes, zero dislike and without and comments.\n"
    )
    posts = requests.get(url=f"{ip}posts/Tech")
    for idx, post in enumerate(json.loads(posts.content)):
        print(f"Post {idx + 1}: {post}")


def tc8(ip, user_1, user_2, user_3, user_4):
    # todo: need to add authentication
    print(
        f"TEST CASE: {user_1} and {user_2} 'like' {user_3}'s post in the Tech topic.\n"
    )

    first_reaction = {
        "like_or_dislike": "Like",
        "comment": "",
        "author": pizza_data.USER_1_ID,
        "post": pizza_data.USER_3_POST_ID,
    }
    post_1 = requests.post(url=f"{ip}add-reaction", json=first_reaction)
    print(f"Status code of first post to 'add-reaction': {post_1.status_code}")

    second_reaction = {
        "like_or_dislike": "Like",
        "comment": "",
        "author": pizza_data.USER_2_ID,
        "post": pizza_data.USER_3_POST_ID,
    }
    post_2 = requests.post(url=f"{ip}add-reaction", json=second_reaction)
    print(f"Status code of second post to 'add-reaction': {post_2.status_code}")


def tc9(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_4} 'likes' {user_2}'s post and 'dislikes' {user_3}'s post in the Tech "
        f"topic.\n"
    )

    first_reaction = {
        "like_or_dislike": "Like",
        "comment": "",
        "author": pizza_data.USER_4_ID,
        "post": pizza_data.USER_2_POST_ID,
    }
    post_1 = requests.post(url=f"{ip}add-reaction", json=first_reaction)
    print(f"Status code of first post to 'add-reaction': {post_1.status_code}")

    second_reaction = {
        "like_or_dislike": "Dislike",
        "comment": "",
        "author": pizza_data.USER_4_ID,
        "post": pizza_data.USER_3_POST_ID,
    }
    post_2 = requests.post(url=f"{ip}add-reaction", json=second_reaction)
    print(f"Status code of second post to 'add-reaction': {post_2.status_code}")


def tc10(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_2} browses all the available posts in the Tech topic; at this stage he "
        f"can see the number of likes and dislikes for each post ({user_3} has 2 likes and 1 "
        f"dislike and {user_2} has 1 like). There are no comments made yet.\n"
    )

    posts = requests.get(url=f"{ip}posts/Tech")
    for idx, post in enumerate(json.loads(posts.content)):
        print(f"Post {idx + 1}: {post}")


def tc11(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_3} likes her post in the Tech topic. This call should be unsuccessful, "
        "as in Pizza a post owner cannot like their own messages.\n"
    )

    print("SKIPPED")


def tc12(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_1} and {user_2} comment on {user_3}'s post in the Tech topic in a "
        f"round-robin fashion (one after the other adding at least 2 comments each).\n"
    )

    def add_reaction(user_, idx, comment):
        reaction = {
            "like_or_dislike": "",
            "comment": comment,
            "author": user_,
            "post": pizza_data.USER_3_POST_ID,
        }
        post = requests.post(url=f"{ip}add-reaction", json=reaction)
        print(f"add reaction {idx +1} status code: {post.status_code}")

    for idx, user in enumerate(
        [
            pizza_data.USER_1_ID,
            pizza_data.USER_2_ID,
            pizza_data.USER_1_ID,
            pizza_data.USER_2_ID,
        ]
    ):
        add_reaction(user, idx, comment=f"cool comment number {idx + 1}")


def tc13(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_2} browses all the available posts in the Tech topic; at this stage "
        f"he can see the number of like and dislikes of each post and the comments made.\n"
    )

    posts = requests.get(url=f"{ip}posts/Tech")
    for idx, post in enumerate(json.loads(posts.content)):
        print(f"Post {idx + 1}: {post}")


def tc14(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_4} posts a message in the Health topic with an expiration time using "
        "her token.\n"
    )

    data = {
        "expires_at": f"{dt.now() + datetime.timedelta(seconds=5)}",
        "author": pizza_data.USER_4_ID,
        "title": "Post 4",
        "body": "A cool post about something health related",
        "topics": ["Health"],
    }
    post = requests.post(url=f"{ip}create-post", json=data)
    post_id = json.loads(post.content)["id"]
    pizza_data.set_user_4_post_id(post_id)
    print(f"Status code of post: {post.status_code}")


def tc15(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_3} browses all the available posts in the Health topic; at this stage "
        f"she can only {user_4}'s post.\n"
    )
    posts = requests.get(url=f"{ip}posts/Health")
    for idx, post in enumerate(json.loads(posts.content)):
        print(f"Post {idx + 1}: {post}")


def tc16(ip, user_1, user_2, user_3, user_4):
    print(f"TEST CASE: {user_3} comments on {user_4}'s post in the Health topic.\n")

    reaction = {
        "like_or_dislike": "",
        "comment": "A reaction about some post about health",
        "author": pizza_data.USER_3_ID,
        "post": pizza_data.USER_4_POST_ID,
    }
    post = requests.post(url=f"{ip}add-reaction", json=reaction)
    print(f"Status code of post to 'add-reaction': {post.status_code}")


def tc17(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_3} dislikes {user_4}'s message in the Health topic after the end of "
        f"the post expiration time. This should fail.\n"
    )

    # We put the script to sleep for 6 seconds to ensure that the post will have expired
    print("sleeping for 6 seconds...")
    time.sleep(6)

    reaction = {
        "like_or_dislike": "Dislike",
        "comment": "",
        "author": pizza_data.USER_3_ID,
        "post": pizza_data.USER_4_POST_ID,
    }
    reaction = requests.post(url=f"{ip}add-reaction", json=reaction)

    print(
        "The post to 'add-reaction' should return a 400 as the post is no longer accepting "
        "request"
    )
    print(f"Status code of post to 'add-reaction': {reaction.status_code}")
    print(
        f"Returned message of post to 'add-reaction': "
        f"{json.loads(reaction.content)['non_field_errors'][0]}"
    )


def tc18(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_4} browses all the messages in the Health topic. There should be only "
        f"one post (his own) with one comment ({user_3}'s).\n"
    )

    posts = requests.get(url=f"{ip}posts/Health")
    for idx, post in enumerate(json.loads(posts.content)):
        print(f"Post {idx + 1}: {post}")


def tc19(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_2} browses all the expired messages in the Sport topic. These should "
        f"be empty.\n"
    )

    print("SKIPPED")


def tc20(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_4} queries fo an active post having the highest interest (maximum sum "
        f"of like and dislikes in the Tech topic. This should be {user_3}'s post.\n"
    )

    print("SKIPPED")


if __name__ == "__main__":
    IP = "http://127.0.0.1:8000/"
    TEST_CASES = [value for key, value in globals().items() if key.startswith("tc")]
    test_case_runner(IP, TEST_CASES)
