import pytest
from community_database.models import init_db, Community, Post

# Basic testing fixture for an in-memory SQLite DB
@pytest.fixture
def db_session():
    session = init_db("sqlite:///:memory:")
    yield session
    session.close()

def test_community_creation(db_session):
    community = Community(
        name="Alexandria Real Estate",
        platform="Facebook Groups",
        url="https://facebook.com/groups/alex-realestate",
        governorate="Alexandria",
        status="Needs Review"
    )
    db_session.add(community)
    db_session.commit()
    
    fetched = db_session.query(Community).filter_by(name="Alexandria Real Estate").first()
    assert fetched is not None
    assert fetched.governorate == "Alexandria"

def test_post_drafting(db_session):
    post = Post(
        content="عروض حصرية لاهل اسكندرية!",
        language="Egyptian Arabic",
        status="Needs Approval"
    )
    db_session.add(post)
    db_session.commit()
    
    fetched = db_session.query(Post).first()
    assert fetched is not None
    assert "اسكندرية" in fetched.content
    assert fetched.status == "Needs Approval"
