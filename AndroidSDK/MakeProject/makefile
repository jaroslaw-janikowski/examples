PROJECT_NAME = aspec
PROJECT_DIR = ~/workspace/aspec
ANDROID_HOME = ~/apps/android-sdk-linux
BUILD_TOOLS = 24.0.1
JACK = java -jar $(ANDROID_HOME)/build-tools/$(BUILD_TOOLS)/jack.jar
AAPT = $(ANDROID_HOME)/build-tools/$(BUILD_TOOLS)/aapt
ZIPALIGN = $(ANDROID_HOME)/build-tools/$(BUILD_TOOLS)/zipalign

debug: clean generate_R compile_dex generate_apk sign_debug
release: clean generate_R compile_dex generate_apk sign_release align_apk

compile_dex:
	$(JACK) --classpath $(ANDROID_HOME)/platforms/android-24/android.jar:$(ANDROID_HOME)/extras/android/support/v4/android-support-v4.jar --output-dex $(PROJECT_DIR)/bin --import $(ANDROID_HOME)/extras/android/support/v4/android-support-v4.jar --import-resource $(PROJECT_DIR)/res $(PROJECT_DIR)/src $(PROJECT_DIR)/gen

generate_R:
	$(AAPT) package -v -f -m -S $(PROJECT_DIR)/res -J $(PROJECT_DIR)/gen -M $(PROJECT_DIR)/AndroidManifest.xml -I $(ANDROID_HOME)/platforms/android-24/android.jar

generate_apk:
	$(AAPT) package -v -f -M $(PROJECT_DIR)/AndroidManifest.xml -S $(PROJECT_DIR)/res -I $(ANDROID_HOME)/platforms/android-24/android.jar -I $(ANDROID_HOME)/extras/android/support/v4/android-support-v4.jar -F $(PROJECT_DIR)/bin/$(PROJECT_NAME).unsigned.apk
	# $(AAPT) add -f $(PROJECT_NAME).unsigned.apk $(PROJECT_DIR)/bin/classes.dex
	jar -uf $(PROJECT_DIR)/bin/$(PROJECT_NAME).unsigned.apk -C $(PROJECT_DIR)/bin/ classes.dex

sign_debug:
	jarsigner -storepass android -keypass android -keystore ~/.android/debug.keystore -signedjar $(PROJECT_DIR)/bin/$(PROJECT_NAME).debug.apk $(PROJECT_DIR)/bin/$(PROJECT_NAME).unsigned.apk AndroidDebugKey

sign_release:
	@echo "Give storepass keypass and alias:"
	@read STORE_PASS KEY_PASS ALIAS; \
	keytool -genkey -v -keystore $(PROJECT_DIR)/release.keystore -storepass $$STORE_PASS -alias $$ALIAS -keypass $$KEY_PASS; \
	jarsigner -storepass $$STORE_PASS -keypass $$KEY_PASS -keystore $(PROJECT_DIR)/release.keystore -signedjar $(PROJECT_DIR)/bin/$(PROJECT_NAME).release.apk $(PROJECT_DIR)/bin/$(PROJECT_NAME).unsigned.apk $$ALIAS

align_apk:
	$(ZIPALIGN) -v -f 4 $(PROJECT_DIR)/bin/$(PROJECT_NAME).release.apk $(PROJECT_DIR)/bin/$(PROJECT_NAME).apk

generate_debug_key:
	keytool -genkey -v -keystore ~/.android/debug.keystore -storepass android -alias androiddebugkey -keypass android -dname "CN=Android Debug,O=Android,C=US"

clean:
	rm -rf $(PROJECT_DIR)/bin/*
	rm -rf $(PROJECT_DIR)/gen/*
	-rm $(PROJECT_DIR)/release.keystore
