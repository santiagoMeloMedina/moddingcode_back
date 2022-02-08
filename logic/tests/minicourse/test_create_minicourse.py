import os
from unittest.mock import patch, Mock
import pytest


_DEFAULT_ENVIRONMENT = {
    "MINICOURSE_BUCKET_NAME": "",
    "MINICOURSE_TABLE_NAME": "",
    "CATEGORY_TABLE_NAME": "",
    "THUMB_UPLOAD_EXPIRE_TIME": "300",
}


MOCK_MINICOURSE_DATA = {
    "name": "test_minicourse",
    "thumb_ext": "png",
    "category_id": "1",
}
MOCK_MINICOURSE_ID = "12341234-413243124"
MOCK_MINICOURSE_THUMB_UPLOAD_URL = "http://thumb"


@pytest.mark.unit
@patch.dict(os.environ, _DEFAULT_ENVIRONMENT)
@patch(
    "modding.common.repo.Repository.put_presigned_url",
    return_value=MOCK_MINICOURSE_THUMB_UPLOAD_URL,
)
def test_build_minicourse(put_presigned_url: Mock):
    from modding.minicourse import create_minicourse as subject, models

    mock_minicourse_with_id = {**MOCK_MINICOURSE_DATA, "id": MOCK_MINICOURSE_ID}

    minicourse, upload_url = subject.build_and_get_upload_url(**mock_minicourse_with_id)

    assert models.Minicourse(**mock_minicourse_with_id) == minicourse
    assert upload_url == MOCK_MINICOURSE_THUMB_UPLOAD_URL

    put_presigned_url.assert_called_once_with(
        "thumbs",
        f"{MOCK_MINICOURSE_ID}.{minicourse.thumb_ext}",
        300,
    )


@pytest.mark.unit
@patch.dict(os.environ, _DEFAULT_ENVIRONMENT)
@patch(
    "modding.common.repo.Repository.put_presigned_url",
    return_value=MOCK_MINICOURSE_THUMB_UPLOAD_URL,
)
@patch("modding.minicourse.category.repository.CategoryRepository.get_item_by_id")
@patch("modding.common.repo.Repository.save_on_table")
def test_create_minicourse(
    save_on_table: Mock,
    category_get_item_by_id: Mock,
    put_presigned_url: Mock,
):
    from modding.minicourse import create_minicourse as subject, models

    class AnyStr(str):
        def __eq__(self, *args, **kwargs) -> bool:
            return True

    MOCK_CATEGORY = models.Category(id="cat1", name="category1")

    category_get_item_by_id.return_value = MOCK_CATEGORY

    minicourse, upload_url = subject.create_minicourse(**MOCK_MINICOURSE_DATA)

    assert len(minicourse.id) > 0
    assert minicourse.id.startswith(minicourse.category_id)

    mock_minicourse = models.Minicourse(
        id=AnyStr(),
        category_id=MOCK_CATEGORY.id,
        thumb_ext=MOCK_MINICOURSE_DATA.get("thumb_ext"),
        name=MOCK_MINICOURSE_DATA.get("name"),
    )

    assert minicourse == mock_minicourse
    save_on_table.assert_called_once_with(minicourse)