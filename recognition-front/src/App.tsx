import './App.css';
import ImageUploader from './ImageUploader';

function App() {
  return (
    <div>
      <header className="bg-blue-600 p-4 text-white">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-3xl font-bold">AWS Icon Recognition</h1>
        </div>
      </header>
      <ImageUploader />
    </div>
  );
}

export default App;
