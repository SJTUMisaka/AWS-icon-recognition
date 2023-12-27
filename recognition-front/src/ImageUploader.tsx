import React, { useState } from 'react';
import axios from 'axios';

const ImageUploader: React.FC = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploadResult, setUploadResult] = useState<{ class: string; probability: number } | null>(null);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
            setSelectedFile(event.target.files[0]);
        }
    };

    const handleSubmit = async () => {
        if (selectedFile) {
            const formData = new FormData();
            formData.append('file', selectedFile);

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
        }
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleSubmit}>Upload</button>
            {uploadResult && (
                <div>
                    <p>Class: {uploadResult.class}</p>
                    <p>Probability: {uploadResult.probability.toFixed(2)}</p>
                </div>
            )}
        </div>
    );
};

export default ImageUploader;
