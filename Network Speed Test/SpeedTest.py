import speedtest

def perform_speed_test():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000      # Convert to Mbps
    ping = st.results.ping
    return download_speed, upload_speed, ping

if __name__ == "__main__":
    download, upload, ping = perform_speed_test()
    print(f"Download Speed: {download:.2f} Mbps")
    print(f"Upload Speed: {upload:.2f} Mbps")
    print(f"Ping: {ping} ms")
