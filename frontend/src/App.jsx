import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import ReviewSession from "./components/ReviewSession";
import CardList from "./components/CardList";
import CardForm from "./components/CardForm";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/review" element={<ReviewSession />} />
        <Route path="/cards" element={<CardList />} />
        <Route path="/cards/new" element={<CardForm />} />
        <Route path="/cards/:id" element={<CardForm />} />
      </Routes>
    </BrowserRouter>
  );
}
