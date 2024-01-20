<div align="center">
  <h2> Captcha_Analyzer </h2>
  <h5> Using a controlled chrome browser, the code Browsing to the site, Capturing the captcha, Filtering all the noise from the text, Translating it to a text output, and finally Sending the result to the website </h5>
</div>

<br />

> [!NOTE]
> For now, this code is working only with "Zone-H" website, as other websites may use other captchas and it also will require changes in the configurations file so the program will know where in the page each elemnt is located

<br />

<div align="center">
  
  ![Captcha Filtering Example][Project-UI]
  
</div>


## Configuration File
Almost any important data inside the code can be reconfigured directly from the "Analyzer Configurations.ini" file without the need to interact with the code itself.

In case of a missing file, the code will create it with the default data that can be found inside "def_config_file.py". In case of a missing section or a specific key in one of the file sections, the code will replace the entire section with the default data (the rest of the file will be untouched).

**Analyzer Configurations.ini** - Detailed
```
[general]
history_dir = Data/History                         # Directory of all captured captchas and the detection results for a future ML model
achieved_captcha_file = Data/New Captcha.png       # Where to save the current tested captcha
cleared_captcha_file = Data/Cleared Captcha.png    # Where to save the current filtered captcha
captcha_attempts = 20                              # How many attempts to detect the captcha

[website]
website_url = https://www.zone-h.org/archive?hz=1            # The URL with the captcha
captcha_id = cryptogram                                      # html captcha ID
text_field_name = captcha                                    # html text field Name
submit_button_xpath = //*[@id='propdeface']/form/input[2]    # html submit button XPath

[filter]
use_median = True                    # Use the Median Blur filter on the captcha (good for salt-papper noise)
use_dilate_erode = False             # Use the Dilation & Erosion filters on the captcha (can used without the median or as addition to it)
median_kernel_size = 5               # Kernel/Mask size for the Median filter (use only odd numbers)
dilate_erode_kernel_size = (3, 3)    # Kernel/Mask size for the Dilation & Erosion filters
dilate_erode_iterations = 1          # How many iterations for each Dilation & Erosion filter

[client]
client_url = https://docparser-text-captcha-breaker.hf.space/    # The picture to text client URL
client_access_attempts = 3                                       # Client access attempts, in case of a timeout from the client in his response
client_access_delay = 0.25                                       # Delay between the access attempts to the client

[debug]
show_comparison = True    # Show the filtering process picture

[local_test]
test_type = Model Test                                 # Choice the test type:
                                                         # "Model Test" - Test the analysis model constancy
                                                         # "Filter Test" - Test different filtering steps
test_database_dir = Data/Test Database                 # Directory of all the desired captchas to run the test on
test_client_access_delay = 0.5                         # Same as "client_access_delay" but specific for the local test
model_test_repeats = 5                                 # How many times to run the Model Test on each captcha
filter_1_dir = Data\Methods Test\Filter 1              # Directory to save the results of using only the Median filter
filters_1_2_3_dir = Data\Methods Test\Filters 1,2,3    # Directory to save the results of using all the filters together
filters_2_3_dir = Data\Methods Test\Filters 2,3        # Directory to save the results of using only the Dilation & Erosion filters
```

## Local Tester


<!-- MARKDOWN LINKS & IMAGES -->
[Project-UI]: Pictures/Captcha_Filtering_Example.png
