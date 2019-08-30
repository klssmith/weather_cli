import requests
import requests_mock
import weather_cli.weather


def test_no_internet(capsys):
    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             '3772', 'api key'),
            exc=requests.exceptions.ConnectTimeout,
        )
        weather_cli.weather.main(['observations', '3772'])
        captured = capsys.readouterr()


    assert captured == 'Error - no internet connection'
