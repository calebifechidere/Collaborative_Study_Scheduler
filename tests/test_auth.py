import services


def test_register_user_uses_hashed_password(monkeypatch):
    captured = {}

    def fake_execute_with_row(query, params):
        captured["query"] = query
        captured["params"] = params
        return (7,)

    monkeypatch.setattr(services, "execute_with_row", fake_execute_with_row)

    user_id = services.register_user("Ada Lovelace", "ada@example.com", "Computer Science", "300", "secret123")

    assert user_id == {"user_id": 7}
    assert captured["query"].strip().startswith("INSERT INTO users")
    assert captured["params"][0:4] == ("Ada Lovelace", "ada@example.com", "Computer Science", "300")
    assert captured["params"][4] == "secret123"
