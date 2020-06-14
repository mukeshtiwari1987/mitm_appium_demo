#### One Time System set up before running Appium scripts
* Clone the repository and type `python3 -m venv venv`
* Run the following command `pip3 install -r requirements`
* Install Android Studio
* Download Emulator Nexus 6 with API 27. Do not download Pixel emulator and emulator above API 28
* Verify if emulator name with followinig command `emulator -list-avds`
* Start the emulator with followinig command `emulator -avd Nexus_6_API_27 -writable-system &`
* Run the following one by one to install MITM proxy on the emulator at Android's system level
	````
	adb root
	adb remount
	ca=~/.mitmproxy/mitmproxy-ca-cert.pem
	hash=$(openssl x509 -noout -subject_hash_old -in $ca)
	adb push $ca /system/etc/security/cacerts/$hash.0
	````

#### Appium Set up
* Start Appium with following command ```appium --relaxed-security --log-timestamp --local-timezone```

#### MITMProxy Set up
* Start MITMProxy with following command ```mitmdump -s mitm_main.py --ignore-hosts '^(?![0-9\.]+:)(?!([^\.:]+\.)*netcoresmartech\.com:)'```

#### Execute Appium script
* Start appium script with following command ```pytest -s test_pn.py```

#### Working Demo
<a href="https://drive.google.com/file/d/1m-wKlbo8GTsUyo0onphXTSt__fd0ARGW/view?usp=sharing" target="_blank">
<img src="https://i.ibb.co/JdyM5f1/vlcsnap-2020-06-14-01h29m24s194.png" 
alt="demo image" width="480" height="360" border="50" />
</a>
