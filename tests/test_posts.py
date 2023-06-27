import pytest

from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    posts = list(map(lambda post: schemas.PostOut(**post), res.json()))

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 222


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 200


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/125115")

    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    test_post_id = test_posts[0].id
    res = authorized_client.get(f"/posts/{test_post_id}")
    post = schemas.PostOut(**res.json())

    assert res.status_code == 200
    assert post.Post.id == test_post_id
    assert post.Post.content == test_posts[0].content


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 200


@pytest.mark.parametrize("title, content, published", [
    ("first title", "some first content", True),
    ("second title", "second content", False),
    ("third title", "3rd content", True)
])
def test_create_post(authorized_client, token, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title


@pytest.mark.parametrize("title, content, published", [
    ("first title", "some first content", True),
])
def test_unauthorized_user_create_post(client, test_posts, title, content, published):
    res = client.post("/posts/", json={"title": title, "content": content, "published": published})

    assert res.status_code == 401


def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_another_user_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[2].id}")

    assert res.status_code == 403


def test_delete_not_exist_post(authorized_client, test_posts):
    res = authorized_client.delete("/posts/124")

    assert res.status_code == 404


def test_update_post(authorized_client, test_posts):
    data = {"title": "new title", "content": "updated content"}
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.Post(**res.json())

    assert updated_post.id == test_posts[0].id
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_unauthorized_user_update_post(client, test_posts):
    data = {"title": "new title", "content": "updated content"}
    res = client.put(f"/posts/{test_posts[0].id}", json=data)

    assert res.status_code == 401


def test_other_user_update_post(authorized_client, test_posts):
    data = {"title": "new title", "content": "updated content"}
    res = authorized_client.put(f"/posts/{test_posts[2].id}", json=data)

    assert res.status_code == 403


def test_update_not_exist_post(authorized_client, test_posts):
    data = {"title": "new title", "content": "updated content"}
    res = authorized_client.put("/posts/124", json=data)

    assert res.status_code == 404
