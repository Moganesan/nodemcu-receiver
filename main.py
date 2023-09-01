import http.server
import socketserver
import pyautogui
import os
import time
import cv2
import numpy as np

PORT = 8083  # Choose a port number

class CommandHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Server Running')
        if self.path.startswith('/welcome'):
            # Replace with the path to your Spotify executable
            brave_path = "C:\\Users\\htmog\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
            try:
                os.system(f'start "" "{brave_path}"')
                print(f"Opened Brave browser successfully.")
                time.sleep(2)
                pyautogui.write("youtube.com")
                pyautogui.press("enter")
                time.sleep(3)
                pyautogui.screenshot("screenshot.png")
                screenshot = cv2.imread("screenshot.png")
                template = cv2.imread("searchBox.PNG")
                x_coordinate, y_coordinate, res = self.getImageCoordinates(screenshot, template, 0.5)
                if (res == 0):
                    print("No Match found")
                pyautogui.click(x_coordinate, y_coordinate)
                pyautogui.write("moganesan")
                time.sleep(2)
                pyautogui.press("enter")
                time.sleep(2)
                pyautogui.screenshot("searchResult.png")
                searchResult = cv2.imread("searchResult.png")
                targetResult = cv2.imread("channel.PNG")

                foundChannelXCoordinate, foundChannelYCoordinate, foundChannelRes = self.getImageCoordinates(
                    searchResult, targetResult, 0.5)
                if (foundChannelRes == 0):
                    print("No Channel Found")
                pyautogui.click(foundChannelXCoordinate, foundChannelYCoordinate + 50)
                time.sleep(3)
                pyautogui.screenshot("channelPage.png")
                channelPageImage = cv2.imread("channelPage.png")
                videoButton = cv2.imread("videoButton.PNG")

                foundVideoButtonXCoordinate, foundVideoButtonYCoordinate, foundVideoButtonRes = self.getImageCoordinates(
                    channelPageImage, videoButton, 0.5)
                if (foundVideoButtonRes == 0):
                    print("Video Button Not Found")
                pyautogui.click(foundVideoButtonXCoordinate + 100, foundVideoButtonYCoordinate)
                time.sleep(1)
                pyautogui.click(foundVideoButtonRes + 1000, foundVideoButtonYCoordinate + 200)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Command executed')
    def getImageCoordinates(self,screenshot,template,threshold):
        # perform template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        # Check if any matches were found
        if loc[0].size > 0:
            # Get the coordinates of the first match (you can iterate through loc to find more matches)
            match_x, match_y = loc[1][0], loc[0][0]  # Note the change here
            # Calculate the center of the matched region
            match_center_x = match_x + template.shape[1] // 2
            match_center_y = match_y + template.shape[0] // 2
            return match_center_x, match_center_y, 1
        else:
            return 0


with socketserver.TCPServer(("", PORT), CommandHandler) as httpd:
    print(f"Serving on port {PORT}")

    # Start the server indefinitely (remove the serve_forever call from the 'with' block)
    httpd.serve_forever()