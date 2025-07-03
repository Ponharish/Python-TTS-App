# Python-TTS-App

## Setting Up the App with Amazon Polly

Follow these steps to set up your app with Amazon Polly:

### 1. Sign up for an AWS Account
- Go to the [AWS Sign Up Page](https://aws.amazon.com) and sign up for a new account.
- **Note**: Signing up requires a credit card. A fee of **USD $1** will be charged during the sign-up process, but this amount will be refunded.

### 2. Enable Polly Service
- After signing up, log in to your AWS Management Console.
- Navigate to the **Polly** service (you can search for **Polly** in the search bar).
- Enable the service to start using Amazon Polly's Text-to-Speech functionality.

### 3. Create IAM User with Programmatic Access
- Go to the **IAM** (Identity and Access Management) service in the AWS console.
- Click on **Users** in the left-hand menu, then click on **Add user**.
- Enter a username for your new IAM user (e.g., `pollyUser`).
- Under **Access type**, select **Programmatic access**.
- Click **Next: Permissions**.

### 4. Assign Permissions to the IAM User
- On the **Set Permissions** page, you can either assign existing permissions or create a custom policy.
- You can choose to directly assign permissions like **AmazonPollyFullAccess** or create a custom policy for more control over permissions.
- Once done, click **Next: Tags**, add tags if needed, then click **Next: Review**.
- Finally, click **Create user**.

### 5. Save the AWS Credentials
- After the IAM user is created, you will see the **Access Key ID** and **Secret Access Key**.
- **Important**: Store these credentials securely.

---

## Using the Application

<br>

1. **Download the `Python TTS.app` File**:
   - Download the latest version of **`Python TTS.app`** file from the provided [link](https://github.com/Ponharish/Python-TTS-App/releases/tag/Week_4).
   - **Double-click** the `.app` file to open it.

2. **Register your AWS Credentials**:
   - Upon opening the app, a window will pop up prompting your AWS Credentials
   ![AWS Credentials Registration page](./pictures/configureKeys.png)
     - **AWS Access Key**: Your **Access Key ID** from the AWS IAM user you created.
     - **AWS Secret Key**: Your **Secret Access Key** associated with the IAM user.

3. **Main Page**:
   - Upon completing the registration, the main page will load
   ![Main page](./pictures/mainPage.png)

4. **Convert Text to Speech**:
  - In the main page, first select the region that is to be used
   ![Main page - region selection](./pictures/mainPage_SelectRegion.png)
  - Then specify the **Engine** to be used (Standard or Neural)
    - **Standard Engine**: This engine uses a basic synthetic voice that may sound more robotic. It's efficient and works for most basic speech needs.
    - **Neural Engine**: This engine provides a more **natural-sounding voice** that is much closer to human speech, offering better intonation and fluidity.
  - Choose the **language** of the text that is to be converted to speech. The list of available languages shown is based on the selected region and engine.
  - Choose the **voice** that would read the given text. The list of available voices shown is based on the selected region, engine and language.
  - Choose the **Input Text Type**:
    - **Text**: Normal text that will be read aloud **as-is**, without any special processing.
    - **SSML (Speech Synthesis Markup Language)**: This option allows you to use **SSML** tags to control the speech characteristics like pauses, pitch, and volume. The input will be processed before converting to speech.
  - Enter the Text to be Converted to Speech:
    - Type in the **text** (or SSML) that you want to be converted to speech. This is the content that will be spoken aloud by Amazon Polly.

  - **Click on Submit**:
  ![Main page - submit](./pictures/mainPage_Submit.png)
    - After entering all the necessary details, click on the **"Submit"** button.
    - The app will generate the audio and **play it through your speakers**.

5. **Signing in as another user**:
  - Click on **Reconfigure Keys**, which will open up the window for registering keys. Using this window, the new keys can be entered and they will be saved.


### Troubleshooting

Credential Registration Page
![AWS Credentials Registration page Error](./pictures/configureKeys_Error.png)
- **Invalid AWS Access Key**:  
  Ensure that the **AWS Access Key** entered is **valid**. Double-check that there are **no extra spaces or incorrect characters** before or after the key.

- **Invalid AWS Secret Key**:  
  Verify that the **AWS Secret Key** is correct. Make sure there are **no extra spaces** or **incorrect characters** in the key, especially at the start or end.


Main Page

- **Input Text is Too Long**:  
  The app has a limit of **2990 characters** for the text input. If the provided input exceeds this limit, you will see an error message prompting you to shorten the text.

- **Empty Text Field**:  
  Make sure that the **text field** is not empty. The app will not proceed if no text is provided to convert into speech.

- **Invalid SSML Input**:  
  This error occurs only if **SSML** is selected as the input type. The input must be a **valid SSML format**. Ensure that SSML tags (e.g., `<speak>`, `<break time="500ms"/>`) are properly structured and closed.

---