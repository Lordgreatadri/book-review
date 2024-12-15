
import uuid
from src.tags.schemas import TagCreateModel


tag_prefix =f"/api/v1/tags"

def test_get_all_tags(fake_session, fake_tag_service, test_client):
    response = test_client.get(f"{tag_prefix}/")

    assert fake_tag_service.get_tags_called_once()
    assert fake_tag_service.get_tags_called_once_with(fake_session)



def test_add_tag(fake_session, fake_tag_service, test_client):
    data = {
        "name": "Python"
    }

    response = test_client.post(f"{tag_prefix}/", json=data)
    add_tag_data = TagCreateModel(**data)

    assert fake_tag_service.add_tag_called_once()
    assert fake_tag_service.add_tag_called_once_with(fake_session, add_tag_data)



def test_add_tags_to_book(fake_session, fake_tag_service, test_book, test_client):

    test_tag = {"tags": [{"uid":str(uuid.uuid4()) ,"name": "Python"}]}
    response = test_client.post(f"{tag_prefix}/{test_book.uid}/tags",json=test_tag)

    assert fake_tag_service.add_tags_to_book_called_once()
    assert fake_tag_service.add_tags_to_book_called_once_with(test_book.uid, test_tag, fake_session)




def test_update_tag(fake_session, fake_tag_service, test_client, test_tag):
    data = {
        "name": "Updated Python"
    }
    response = test_client.put(f"{tag_prefix}/{test_tag.uid}", json=data)

    assert fake_tag_service.update_tag_called_once()
    assert fake_tag_service.update_tag_called_once_with(test_tag.uid, data, fake_session)



def test_delete_tag(fake_session, fake_tag_service, test_tag, test_client):
    response = test_client.delete(f"{tag_prefix}/{test_tag.uid}")
    assert fake_tag_service.delete_tag_called_once()
    assert fake_tag_service.delete_tag_called_once_with(test_tag.uid, fake_session)

    # check if tag is deleted by trying to get it
    response = test_client.get(f"{tag_prefix}/{test_tag.uid}")
    # assert response.status_code == 404