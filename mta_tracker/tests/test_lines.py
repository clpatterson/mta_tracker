from flask import url_for


class TestLineStatus(object):
    def test_linestatus_for_valid_input(self, client):
        """
        Linestatus endpoint should return 200 status code and
        json response.
        """
        response = client.get(url_for("status") + "?line=l")
        json_response = response.get_json()

        assert response.status_code == 200
        assert "line" in json_response["response"].keys()

    def test_linestatus_for_invalid_input(self, client):
        """Linestatus endpoint should return 404 status code."""
        response = client.get(url_for("status") + "?line=h")

        assert response.status_code == 404

    def test_linestatus_for_multiple_input(self, client):
        """
        LineStatus endpoint should return 404 status code for
        multiple lines.
        """
        response = client.get(url_for("status") + "?line=lsp")

        assert response.status_code == 404


class TestLineUptime(object):
    def test_lineuptime_for_valid_input(self, client):
        """
        LineUptime endpoint should return 200 status code and
        json response.
        """
        response = client.get(url_for("uptime") + "?line=z")
        json_response = response.get_json()

        assert response.status_code == 200
        assert "line" in json_response["response"].keys()

    def test_lineuptime_for_invalid_input(self, client):
        """
        LineUptime endpoint should return 404 status code for
        nonexistant line.
        """
        response = client.get(url_for("uptime") + "?line=h")

        assert response.status_code == 404

    def test_lineuptime_for_multiple_input(self, client):
        """LineUptime endpoint should return 404 status code for
        multiple lines."""
        response = client.get(url_for("uptime") + "?line=lzj")

        assert response.status_code == 404
