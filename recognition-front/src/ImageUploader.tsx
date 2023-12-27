import React, { useState} from 'react';
import axios from 'axios';

const ImageUploader: React.FC = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [imagePreviewUrl, setImagePreviewUrl] = useState<string | null>(null);
    const [uploadResult, setUploadResult] = useState<{ class: string; probability: number } | null>(null);

    const previewImage = (file: File) => {
        const reader = new FileReader();
        reader.onloadend = () => {
            setImagePreviewUrl(reader.result as string);
        };
        reader.readAsDataURL(file);
    };

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
            if (event.target.files && event.target.files.length > 0) {
                const file = event.target.files[0];
                setSelectedFile(file);
                previewImage(file);
                setUploadResult(null);
            }
        }
    };

    const uploadImage = async (file: File) => {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:8000/uploadfile/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setUploadResult(response.data);
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={() => selectedFile && uploadImage(selectedFile)}>Upload</button>
            {imagePreviewUrl && (
                <div style={{ marginTop: '10px' }}>
                    <img
                        src={imagePreviewUrl}
                        alt="Preview"
                        style={{ width: 'auto', height: '200px' }}
                    />
                </div>
            )}
            <div>
                {uploadResult && (
                    <div>
                        <p>Class: {uploadResult.class}</p>
                        <p>Probability: {uploadResult.probability.toFixed(2)}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ImageUploader;
