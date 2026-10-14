import html
import unittest

from app import app


class LinkedListRouteTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SECRET_KEY="test-secret")
        self.client = app.test_client()

    def test_linked_list_route_uses_the_imported_list(self):
        response = self.client.post(
            "/works/linked-list", data={"action": "append", "value": "Flask"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"1 node", response.data)
        self.assertIn(b"Flask</div>", response.data)

    def test_profile_has_a_distinct_profile_card(self):
        response = self.client.get("/profile")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'class="profile-card"', response.data)
        self.assertIn(b'class="profile-presence"', response.data)

    def test_stack_route_pops_the_latest_value(self):
        self.client.post("/works/stack", data={"action": "push", "value": "first"})
        self.client.post("/works/stack", data={"action": "push", "value": "last"})

        response = self.client.post("/works/stack", data={"action": "pop"})

        self.assertEqual(response.status_code, 200)
        page = html.unescape(response.get_data(as_text=True))
        self.assertIn('Removed "last" from the top of the stack.', page)
        self.assertIn("first</div>", page)

    def test_stack_rejects_values_longer_than_forty_characters(self):
        response = self.client.post(
            "/works/stack", data={"action": "push", "value": "x" * 41}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Stack values must be 40 characters or fewer.", response.data)
        self.assertIn(b"0 values", response.data)


if __name__ == "__main__":
    unittest.main()
