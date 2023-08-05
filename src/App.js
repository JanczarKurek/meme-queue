import './App.css';
import NewsBar from './NewsBar';
import MainContent from './MainContent';
import StatusBar from './StatusBar';

function App() {
  return (
    <div className="App">
      <NewsBar/>
      <MainContent/>
      <StatusBar/>
    </div>
  );
}

export default App;
