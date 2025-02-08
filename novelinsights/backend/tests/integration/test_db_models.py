from novelinsights import models

def test_empty_database_queries(db_session):
    """Test that all models can be queried in an empty database"""
    
    # Dynamically get all models from the novelinsights.models module
    all_models = [
        obj for _, obj in vars(models).items()
        if isinstance(obj, type) and issubclass(obj, models.Base) and obj != models.Base
    ]
    
    for model in all_models:
        assert db_session.query(model).count() == 0
    