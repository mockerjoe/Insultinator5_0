use enigo::{Enigo, Key, Settings};
use pyo3::prelude::*;
use std::thread;
use std::time::Duration;

/// Initializes the Enigo struct and sends the specified text with a simulated Enter key press.
#[pyfunction]
fn send_text_to_chat(text: String, chat_key: String, delay: f64) -> PyResult<()> {
    let mut enigo = Enigo::new(&Settings::default()).expect("Failed to initialize Enigo");

    // Open chat with specified chat key
    if let Some(chat_key) = char::from_u32(chat_key.chars().next().unwrap() as u32) {
        enigo.key_click(Key::Layout(chat_key));
    }

    thread::sleep(Duration::from_secs_f64(delay));

    // Send each line of text
    for line in text.lines() {
        enigo.key_sequence(line);
        thread::sleep(Duration::from_secs_f64(delay));
        enigo.key_click(Key::Return); // Simulate pressing Enter
    }

    Ok(())
}

/// A Python module implemented in Rust.
#[pymodule]
fn insultinator_backend(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(send_text_to_chat, m)?)?;
    Ok(())
}
