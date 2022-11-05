package com.example.imagecapture;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.graphics.Bitmap;
import android.graphics.Typeface;
import android.net.Uri;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.text.SimpleDateFormat;
import java.util.Date;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class UploadImageActivity extends AppCompatActivity{

    private Spinner spinner;
    private ImageView capturedImage;
    private TextView description;
    ProgressBar progressBar;
    String imageCategory;
    Uri capturedImageUri;
    byte[] byteArray;

    @SuppressLint("WrongThread")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        setContentView(R.layout.activity_upload_image);
        capturedImage = findViewById(R.id.imageViewUpload);
        description = findViewById(R.id.descriptionText);
        progressBar = findViewById(R.id.progressBar);


        Bitmap imageBitMap = null;
        Bundle extras = getIntent().getExtras();
        if (extras != null && extras.containsKey("capturedImageUri") && extras.containsKey("capturedImageBitMap")
                && extras.containsKey("capturedImagePath")) {
            capturedImageUri = extras.getParcelable("capturedImageUri");
            imageBitMap = (Bitmap) extras.getParcelable("capturedImageBitMap");
        }
        capturedImage.setImageURI(capturedImageUri);
        //Conversion of bitmap to byte array to send it to server

        InputStream iStream = null;
        try {
            iStream = getContentResolver().openInputStream(capturedImageUri);
            byteArray = getBytes(iStream);
        } catch (IOException e) {
            e.printStackTrace();
        }
        callServer();
        progressBar.setVisibility(View.GONE);
        if(imageCategory != null){
            String text = "Predicted Value:- "+ imageCategory;
            description.setText(text);
            description.setTypeface(null, Typeface.BOLD);
        }
        description.setVisibility(View.VISIBLE);

    }

    private void callServer(){
        OkHttpClient client = new OkHttpClient();
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String filename = "Image_"+timeStamp+".jpeg";
        RequestBody formBody = new MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("image", filename,RequestBody.create(MediaType.parse("image/jpg"), byteArray))
                .build();

        Request request = new Request.Builder().url("http://192.168.0.106:5000/").post(formBody).build();

        Call call = client.newCall(request);
        Response response = null;
        try {
            response = call.execute();
            imageCategory = response.body().string();
        } catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println("Category Selected: "+ imageCategory);
        testMethod(imageCategory);
    }

    private void testMethod(String imageCategory){
        Toast.makeText(this, "Number Category:-  "+ imageCategory, Toast.LENGTH_SHORT).show();
    }


    private byte[] getBytes(InputStream inputStream) throws IOException {
        ByteArrayOutputStream byteBuffer = new ByteArrayOutputStream();
        int bufferSize = 1024;
        byte[] buffer = new byte[bufferSize];

        int len = 0;
        while ((len = inputStream.read(buffer)) != -1) {
            byteBuffer.write(buffer, 0, len);
        }
        return byteBuffer.toByteArray();
    }
}