import requests
import pytest


@pytest.mark.parametrize('url, file_name, correct_status_code', [('http://localhost:8080', 'file_a', 200),
                                                                 ('http://localhost:8081', 'file_b', 200),
                                                                 ('http://localhost:8082', 'file_c', 200)
                                                                ]
                        )
def test_request_for_nodes_containing_files(url: str, file_name: str, correct_status_code: int) -> None:
    response = requests.get(f'{url}/{file_name}')
    assert response.status_code == correct_status_code


@pytest.mark.parametrize('url, file_names', [('http://localhost:8080', ('file_b', 'file_c')),
                                             ('http://localhost:8081', ('file_a', 'file_c')),
                                             ('http://localhost:8082', ('file_b', 'file_a'))
                                            ]
                        )
def test_request_for_nodes_not_containing_files(url: str, file_names: tuple) -> None:
    result_status_codes = []
    for file_name in file_names:
        response = requests.get(f'{url}/{file_name}')
        result_status_codes.append(response.status_code)
    assert result_status_codes == [200, 200]
