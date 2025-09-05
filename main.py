import requests
import json


def send_file_to_wechat_group(file_path, webhook_url):
    """
    通过企业微信机器人Webhook接口发送文件到微信群
    
    :param file_path: 要发送的文件路径
    :param webhook_url: 企业微信机器人的Webhook地址
    """
    # 构造文件上传URL，从webhook_url中提取key参数并指定上传类型为file
    upload_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={webhook_url.split('key=')[1]}&type=file"
    # 以二进制只读模式打开文件，并发送POST请求上传到企业微信服务器
    with open(file_path, 'rb') as file:
        response = requests.post(upload_url, files={'media': file})
        # 从响应中获取媒体文件ID
        media_id = response.json().get('media_id')
    # 检查媒体文件ID是否存在，如果不存在则表示上传失败
    if not media_id:
        print(f"文件上传失败，错误信息: {response.json().get('errmsg')}")
        return
    # 构造发送文件的消息体，指定消息类型为file并包含媒体文件ID
    data = {
        "msgtype": "file",
        "file": {
            "media_id": media_id
        }
    }
    # 发送文件消息到企业微信群
    send_response = requests.post(webhook_url, json=data)
    # 检查发送响应结果，如果errmsg为ok表示发送成功
    if "ok" == send_response.json().get('errmsg'):
        print("文件发送成功")
    else:
        print(f"文件发送失败，错误信息: {send_response.json().get('errmsg')}")


if __name__ == '__main__':
    file_path = "" # 替换为实际文件路径
    webhook_url = ''  # 替换为实际Webhook地址

    send_file_to_wechat_group(file_path, webhook_url)
