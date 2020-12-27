import './App.css';
import Navbar from './Navbar';
import HomeView from './HomeView';


function App() {
  return (
    <div className="App">
      <Navbar />
      <div className="content">
        <HomeView />
      </div>
    </div>
  );
}

export default App;
