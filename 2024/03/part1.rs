use regex::Regex;
use std::{env, fs, io, path::Path};

fn read_input(path: &Path) -> io::Result<String> {
    fs::read_to_string(path)
}

fn solve(program: &String) {
    let re_mul = Regex::new(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)").unwrap();
    let total: u64 = re_mul.captures_iter(program).map(|cap|
        &cap[1].parse::<u64>().unwrap() * &cap[2].parse::<u64>().unwrap()
    ).sum();
    println!("{total}");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    for arg in &args[1..] {
        println!("=== {arg}");
        let data = read_input(Path::new(arg)).expect("reading input");
        solve(&data);
    }
}
