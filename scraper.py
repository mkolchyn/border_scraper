from functions import get_database_connection, fetch_data_from_api, insert_data_into_qla, insert_data_into_bzs


def main():
    """Main function to orchestrate data fetching and insertion."""
    
    '''Populate Queue Length table'''
    try:
        url = "https://belarusborder.by/info/checkpoint?token=bts47d5f-6420-4f74-8f78-42e8e4370cc4"

        data = fetch_data_from_api(url)

        buffer_zone_map = {
            "53d94097-2b34-11ec-8467-ac1f6bf889c0": 1,
            "a9173a85-3fc0-424c-84f0-defa632481e4": 2,
            "b60677d4-8a00-4f93-a781-e129e1692a03": 3,
            "ffe81c11-00d6-11e8-a967-b0dd44bde851": 4
        }

        # Loop through all data and insert based on the mapped zone
        for cp in data['result']:
            if cp['id'] in buffer_zone_map:
                insert_data_into_qla(buffer_zone_map[cp['id']], cp)
                print(f"Total Data for buffer_zone_id {buffer_zone_map[cp['id']]} inserted successfully.")

    except Exception as e:
        print(f"Error: {e}")

    '''Populate Buffer Zone Stats table'''
    try:
        scope = {
            1: "https://belarusborder.by/info/monitoring/statistics?token=test&checkpointId=53d94097-2b34-11ec-8467-ac1f6bf889c0",
            2: "https://belarusborder.by/info/monitoring/statistics?token=test&checkpointId=a9173a85-3fc0-424c-84f0-defa632481e4",
            3: "https://belarusborder.by/info/monitoring/statistics?token=test&checkpointId=b60677d4-8a00-4f93-a781-e129e1692a03",
            4: "https://belarusborder.by/info/monitoring/statistics?token=test&checkpointId=ffe81c11-00d6-11e8-a967-b0dd44bde851",
        }

        for buffer_zone_id, url in scope.items():
            data = fetch_data_from_api(url)
            insert_data_into_bzs(buffer_zone_id, data)
            print(f"Data for buffer_zone_id {buffer_zone_id} inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
