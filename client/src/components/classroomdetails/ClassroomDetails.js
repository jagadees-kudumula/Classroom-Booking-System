// ClassroomDetails.jsx
import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import BookingTable from "./BookingTable";
import "../classroomdetails/ClassroomDetails.css";

const classrooms = {
  GF1: {
    name: "GF1",
    description: "Classroom for advanced learning",
    image:
      "https://images.unsplash.com/photo-1580582932707-520aed937b7b?auto=format&fit=crop&w=800&q=80",
    capacity: 60,
    hasProjector: true,
    hasCable: true,
    hasMic: false,
  },
  GF2: {
    name: "GF2",
    description: "Tech-equipped classroom",
    image:
      "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=800&q=80",
    capacity: 50,
    hasProjector: true,
    hasCable: true,
    hasMic: false,
  },
  GF3: {
    name: "GF3",
    description: "Tech-equipped classroom",
    image:
      "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=800&q=80",
    capacity: 50,
    hasProjector: true,
    hasCable: true,
    hasMic: true,
  },
  GF4: {
    name: "GF4",
    description: "Tech-equipped classroom",
    image:
      "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=800&q=80",
    capacity: 50,
    hasProjector: true,
    hasCable: true,
    hasMic: false,
  },
  GF9: {
    name: "GF9",
    description: "Tech-equipped classroom",
    image:
      "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=800&q=80",
    capacity: 50,
    hasProjector: true,
    hasCable: true,
    hasMic: true,
  },
  GF10: {
    name: "GF10",
    description: "Tech-equipped classroom",
    image:
      "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=800&q=80",
    capacity: 50,
    hasProjector: true,
    hasCable: true,
    hasMic: true,
  },
  smallseminarhall: {
    name: "Small Seminar Hall",
    description: "Ideal for small group discussions",
    image:
      "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=800&q=80",
    capacity: 40,
    hasProjector: true,
    hasCable: true,
    hasMic: true,
  },
  bigseminarhall: {
    name: "Big Seminar Hall",
    description: "Spacious hall for seminars and events",
    image:
      "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=800&q=80",
    capacity: 100,
    hasProjector: true,
    hasCable: true,
    hasMic: true,
  },
};

const ClassroomDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const room = classrooms[id];

  const [showForm, setShowForm] = useState(false);
  const [selectedDay, setSelectedDay] = useState(null);

  // State for today's and tomorrow's bookings
  const [todayBookings, setTodayBookings] = useState([]);
  const [tomorrowBookings, setTomorrowBookings] = useState([]);

  const [formData, setFormData] = useState({
    timing: "",
    subject: "",
    faculty: "",
  });

  if (!room) {
    navigate("/");
    return null;
  }

  // Handle input change in form
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // Handle booking form submission
  const handleSubmit = (e) => {
    e.preventDefault();

    const newBooking = {
      timing: formData.timing,
      subject: formData.subject,
      faculty: formData.faculty,
    };

    if (selectedDay === "Today") {
      setTodayBookings((prev) => [...prev, newBooking]);
    } else if (selectedDay === "Tomorrow") {
      setTomorrowBookings((prev) => [...prev, newBooking]);
    }

    alert(`Classroom booked successfully for ${formData.subject}`);

    setShowForm(false);
    setFormData({
      timing: "",
      subject: "",
      faculty: "",
    });
  };

  const handleBookNow = (day) => {
    setSelectedDay(day);
    setShowForm(true);
  };

  return (
    <div className="classroom-container">
      {/* Back to Home Button */}
    <button className="back-btn" onClick={() => navigate(-1)}>
      ← Back to Previous Page
    </button>
      {/* Top Section */}

      <div className="top-section">
        <img src={room.image} alt={room.name} className="classroom-image" />
        <div className="classroom-info">
          <h2 className="room-title">{room.name}</h2>
          <p className="room-description">{room.description}</p>
          <div className="features">
            <div className="feature-row">
              <span>Capacity:</span>
              <span>{room.capacity}</span>
            </div>
            <div className="feature-row">
              <span>Projector:</span>
              <span style={{ color: room.hasProjector ? "green" : "red" }}>
                {room.hasProjector ? "Available" : "Not Available"}
              </span>
            </div>
            <div className="feature-row">
              <span>Cable:</span>
              <span style={{ color: room.hasCable ? "green" : "red" }}>
                {room.hasCable ? "Available" : "Not Available"}
              </span>
            </div>
            <div className="feature-row">
              <span>Mic:</span>
              <span style={{ color: room.hasMic ? "green" : "red" }}>
                {room.hasMic ? "Available" : "Not Available"}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Section */}
      <div className="bottom-section">
        {/* Scrollable Tables */}
        <div className="booking-table-container">
          <BookingTable title="Today's Bookings" bookings={todayBookings} />
         {/* <button onClick={() => handleBookNow("Today")}>Book Now</button>*/}
          <button className="book-now-btn" onClick={() => handleBookNow("Today")}>
  Book Now
</button>

        </div>

        <div className="booking-table-container">
          <BookingTable title="Tomorrow's Bookings" bookings={tomorrowBookings} />
          <button className="book-now-btn" onClick={() => handleBookNow("Today")}>
  Book Now
</button>

          {/*<button onClick={() => handleBookNow("Tomorrow")}>Book Now</button>*/} 
        </div>
      </div>

      {/* Booking Form */}
      {showForm && (
        <div className="booking-form-overlay">
          <div className="booking-form">
            <h3>Book Classroom - {room.name}</h3>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Timing</label>
                <input
                  type="text"
                  name="timing"
                  value={formData.timing}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Subject</label>
                <input
                  type="text"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Faculty</label>
                <input
                  type="text"
                  name="faculty"
                  value={formData.faculty}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-actions">
                <button type="submit" className="submit-btn">Submit</button>
                <button onClick={() => setShowForm(false)} className="cancel-btn">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClassroomDetails;