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
        for idx, test in enumerate(test_cases):
            call_next_case = input(
                f"Press 'y' to run test case number {idx + 1}. 'n' to skip: "
            )
            if call_next_case == "y":
                print(f"\n---- starting test case: {idx + 1} ----\n")
                test(ip)
                print(f"\n---- test case complete: {idx + 1} ----\n")
            else:
                print(f"\n---- test case skipped: {idx + 1} ----\n")
    print("\n---- TESTS COMPLETE ----")


def tc1(ip):
    print(
        "TEST CASE: Olga, Nick, Mary and Nestor register and are ready to access the Pizza "
        "API.\n"
    )


def tc2(ip):
    print(
        "TEST CASE: Olga, Nick, Mary and Nestor use the oAuth v2 authorisation service to "
        "register and get their tokens.\n"
    )


def tc3(ip):
    print(
        "TEST CASE: Olga makes a call to the API without using her token. This call should be "
        "unsuccessful as the user is unauthorised.\n"
    )


def tc4(ip):
    print(
        "TEST CASE: Olga posts a message in the Tech topic with an expiration time of 5 secs "
        "from now. After the end of the expiration time, the message will not accept any "
        "further user interactions.\n"
    )


def tc5(ip):
    print(
        "TEST CASE: Nick post a message in the Tech topic with an expiration time using his "
        "token.\n"
    )


def tc6(ip):
    print(
        "TEST CASE: Mary posts a message in the Tech topic with an expiration time using her "
        "token.\n"
    )


def tc7(ip):
    print(
        "TEST CASE: Nick and Olga browse all the available posts in the Tech topic, "
        "there should be three posts available with zero likes, zero dislike and without and "
        "comments.\n"
    )


def tc8(ip):
    print("TEST CASE: Nick and Olga 'like' Mary's post in the Tech topic.\n")


def tc9(ip):
    print(
        "TEST CASE: Nestor 'likes' Nick's post and 'dislikes' Mary's post in the Tech topic.\n"
    )


def tc10(ip):
    print(
        "TEST CASE: Nick browses all the available posts in the Tech topic; at this stage he "
        "can see the number of likes and dislikes for each post (Mary has 2 likes and 1 "
        "dislike and Nick has 1 like). There are not comments made yet.\n"
    )


def tc11(ip):
    print(
        "TEST CASE: Mary likes her post in the Tech topic. This call should be unsuccessful, "
        "as in Pizza a post owner cannot like their own messages.\n"
    )


def tc12(ip):
    print(
        "TEST CASE: Nick and Olga comment for Mary's post in the Tech topic in a round-robin "
        "fashion (on after the other adding at least 2 comments each).\n"
    )


def tc13(ip):
    print(
        "TEST CASE: Nick browses  all the available posts in the Tech topic; at this stage he "
        "can see the number of like and dislikes of each post and the comments made.\n"
    )


def tc14(ip):
    print(
        "TEST CASE: Nestor posts a message in the Health topic with an expiration time using "
        "her token.\n"
    )


def tc15(ip):
    print(
        "TEST CASE: Mary browses all the available posts in the Health topic; at this stage "
        "she can only Nestor's post.\n"
    )


def tc16(ip):
    print("TEST CASE: Mary comments on Nestor's post in the Health topic.\n")


def tc17(ip):
    print(
        "TEST CASE: Mary dislikes Nestor's message in the Health topic after the end of the "
        "post expiration time. This should fail.\n"
    )


def tc18(ip):
    print(
        "TEST CASE: Nestor broses all the messages in the Health topic. There should be only "
        "one post (his own) with one comment (Mary's).\n"
    )


def tc19(ip):
    print(
        "TEST CASE: Nick browses all the expired messages in the Sport topic. These should be "
        "empty.\n"
    )


def tc20(ip):
    print(
        "TEST CASE: Nestor queries fo an active post having the highest interest (maximum sum "
        "of like and dislikes in the Tech topic. This should be Mary's post.\n"
    )


if __name__ == "__main__":
    IP = "http://127.0.0.1:8000/"
    TEST_CASES = [value for key, value in globals().items() if key.startswith("tc")]
    test_case_runner(IP, TEST_CASES)
