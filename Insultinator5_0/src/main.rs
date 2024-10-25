use enigo::{
    Button, Coordinate,
    Direction::{Click, Press, Release},
    Enigo, Key, Keyboard, Mouse, Settings,
};
use std::thread;
use std::time::Duration;

fn main() {
    let mut enigo = Enigo::new(&Settings::default()).unwrap();
    // Open chat Key
    enigo.key(Key::Unicode('y'), Click);

    thread::sleep(Duration::from_millis(500));

    // Insert text in chatbox

    enigo.text("Huansohn");

    thread::sleep(Duration::from_millis(500));

    // Simulate pressing the Enter key

    enigo.key(Key::Return, Press); 

    thread::sleep(Duration::from_millis(500));

    enigo.key(Key::Return, Release);
}