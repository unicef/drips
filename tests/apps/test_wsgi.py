def test_wsgi():
    from drips.config.wsgi import application

    assert application
