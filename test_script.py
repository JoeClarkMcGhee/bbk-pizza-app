import requests


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
        "This is a simple app the cycles through 20 test cases that demonstrate the Pizza "
        "API functionality.\n"
    )
    wants_to_run_test_cases = input(
        "Press 'y' if you want to cycle though test cases: "
    )
    if wants_to_run_test_cases == "y":
        user_1 = input("\nUser name 1 (female): ")
        user_2 = input("\nUser name 2 (male): ")
        user_3 = input("\nUser name 3 (female): ")
        user_4 = input("\nUser name 4 (male): ")
        for idx, test in enumerate(test_cases):
            print(f"\n---- starting test case: {idx + 1} ----\n")
            test(ip, user_1, user_2, user_3, user_4)
            print(f"\n---- test case complete: {idx + 1} ----\n")
    print("\n---- TESTS COMPLETE ----")


def tc1(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_1}, {user_2}, {user_3} and {user_4} register and are ready to access "
        f"the Pizza API.\n"
    )

    def create_users():
        for user in [user_1, user_2, user_3, user_4]:
            requests.post(
                url=f"{ip}create-user/",
                json={"username": user, "password": "password123"},
            )
            response = requests.get(url=f"{ip}users/{user}")
            print(
                f"Status code when retrieving details for {user}: {response.status_code}"
            )

    create_users()


def tc2(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_1}, {user_2}, {user_3} and {user_4} use the oAuth v2 authorisation "
        f"service to register and get their tokens.\n"
    )


def tc3(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_1} makes a call to the API without using her token. This call should "
        f"be unsuccessful as the user is unauthorised.\n"
    )


def tc4(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_1} posts a message in the Tech topic with an expiration time of 5 "
        "secs from now. After the end of the expiration time, the message will not accept any "
        "further user interactions.\n"
    )


def tc5(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_2} post a message in the Tech topic with an expiration time using his "
        "token.\n"
    )


def tc6(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_3} posts a message in the Tech topic with an expiration time using her "
        "token.\n"
    )


def tc7(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_2} and {user_1} browse all the available posts in the Tech topic, "
        "there should be three posts available with zero likes, zero dislike and without and "
        "comments.\n"
    )


def tc8(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_2} and {user_1} 'like' {user_3}'s post in the Tech topic.\n"
    )


def tc9(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_4} 'likes' {user_2}'s post and 'dislikes' {user_3}'s post in the Tech "
        f"topic.\n"
    )


def tc10(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_2} browses all the available posts in the Tech topic; at this stage he "
        f"can see the number of likes and dislikes for each post ({user_3} has 2 likes and 1 "
        f"dislike and {user_2} has 1 like). There are not comments made yet.\n"
    )


def tc11(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_3} likes her post in the Tech topic. This call should be unsuccessful, "
        "as in Pizza a post owner cannot like their own messages.\n"
    )


def tc12(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_2} and {user_1} comment for {user_3}'s post in the Tech topic in a "
        f"round-robin fashion (on after the other adding at least 2 comments each).\n"
    )


def tc13(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_2} browses  all the available posts in the Tech topic; at this stage "
        f"he can see the number of like and dislikes of each post and the comments made.\n"
    )


def tc14(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_4} posts a message in the Health topic with an expiration time using "
        "her token.\n"
    )


def tc15(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_3} browses all the available posts in the Health topic; at this stage "
        f"she can only {user_4}'s post.\n"
    )


def tc16(ip, user_1, user_2, user_3, user_4):
    print(f"TEST CASE: {user_3} comments on {user_4}'s post in the Health topic.\n")


def tc17(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_3} dislikes {user_4}'s message in the Health topic after the end of "
        f"the post expiration time. This should fail.\n"
    )


def tc18(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_4} broses all the messages in the Health topic. There should be only "
        f"one post (his own) with one comment ({user_3}'s).\n"
    )


def tc19(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_2} browses all the expired messages in the Sport topic. These should "
        f"be empty.\n"
    )


def tc20(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_4} queries fo an active post having the highest interest (maximum sum "
        f"of like and dislikes in the Tech topic. This should be {user_3}'s post.\n"
    )


if __name__ == "__main__":
    IP = "http://127.0.0.1:8000/"
    TEST_CASES = [value for key, value in globals().items() if key.startswith("tc")]
    test_case_runner(IP, TEST_CASES)
