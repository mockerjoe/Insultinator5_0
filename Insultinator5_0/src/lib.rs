use enigo::{
    Button,
    Coordinate,
    Direction::{Click, Press, Release},
    Enigo,
    Key,
    Keyboard,
    Mouse,
    Settings,
};
use pyo3::prelude::*;
use std::thread;
use std::time::Duration;

/// Initializes the Enigo struct and sends the specified text with a simulated Enter key press.
#[pyfunction]
fn send_text_to_chat(text: String, chat_key: String, delay: f64) -> PyResult<()> {
    let mut enigo = Enigo::new(&Settings::default()).map_err(|_| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Failed to initialize Enigo"))?;

    // Open chat with specified chat key
    if let Some(chat_char) = chat_key.chars().next() {
        enigo.key(Key::Unicode(chat_char), Click);
    } else {
        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid chat key provided"));
    }

    // Delay before sending messages
    thread::sleep(Duration::from_secs_f64(delay));

    // Send each line of text
    for line in text.lines() {
        enigo.text(line);
        thread::sleep(Duration::from_secs_f64(delay));
        enigo.key(Key::Return, Click); // Simulate pressing Enter
    }

    enigo.key(Key::Control, Press);
    enigo.key(Key::Unicode('z'), Click);
    enigo.key(Key::Control, Release);

    Ok(())
}

/// A Python module implemented in Rust.
#[pymodule]
pub fn insultinator_backend(py: Python, m: &PyModule) -> PyResult<()> {
    println!("Rust module loaded");
    m.add_function(wrap_pyfunction!(send_text_to_chat, m)?)?;
    Ok(())
}