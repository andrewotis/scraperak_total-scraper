from datetime import datetime
import boto3, os

async def take_screenshot(page, path, app):
    date_for_path = datetime.now().strftime('%Y-%m-%d_%H')
    if app.get('config').screenshot_storage_type == "local":
        screenshot_path = f"{app.get('config').screenshot_path}/{date_for_path}/{path.replace("f/", "").replace("/", "")}.png"
        await page.screenshot(path=screenshot_path, full_page=True, timeout=app.get('config').timeout)
    elif app.get('config').screenshot_storage_type == "aws_s3":
        filename = f"{date_for_path}/{path.replace("f/", "").replace("/", "")}.png"
        screenshot_path = f"{app.get('config').screenshot_path}/{date_for_path}/{path.replace("f/", "").replace("/", "")}.png"
        await page.screenshot(path=screenshot_path, full_page=True, timeout=app.get('config').timeout)

        s3 = app.get('s3')
        if s3 is None:
            session = boto3.Session(
                aws_access_key_id = os.getenv("AWS_ACCESS_KEY"),
                aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name = 'us-west-2'
            )
            s3 = session.resource("s3")
            app.add('s3', s3)

        try:
            app.get('s3').Bucket(app.get('config').aws_s3_bucket_name).upload_file(screenshot_path, f"screenshots/{date_for_path}/{path.replace("f/", "").replace("/", "")}.png")
            app.get('logger').info(f"Uploaded {screenshot_path} to aws s3")
        except Exception as e:
            app.get('logger').error(f"Problem uploading to s3: {e}")


        try:
            os.remove(screenshot_path)
            print(f"{screenshot_path} has been deleted.")
        except FileNotFoundError:
            print(f"{screenshot_path} does not exist.")
        except PermissionError:
            print(f"Permission denied: Unable to delete {screenshot_path}.")
        except Exception as e:
            print(f"Error occurred: {e}")
    app.get('logger').info(f"Screenshot saved: {screenshot_path}")