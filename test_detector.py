import argparse
import client


def main():
    
    client.connect_to_launcher()
    template = client.get_endpoint_template(client.SPEED)

    template['device_id'] = 14
    template['zone_id'] = 54
    template['license_plate'] = "tabo - prueba"
    template['avg_speed'] = "0"
    template['max_speed'] = "0"
    template['video_url'] = "null"

    
    status = client.post_update(template, client.SPEED)
    client.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rtsp', type=str, default="", help='position')
    parser.add_argument('--id', type=str, default="", help='position2')
    opt = parser.parse_args()

    main()
