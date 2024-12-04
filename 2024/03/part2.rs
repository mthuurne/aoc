use regex::Regex;
use std::{env, fs, io, path::Path};

fn read_input(path: &Path) -> io::Result<String> {
    fs::read_to_string(path)
}

fn solve(program: &String) {
    let re_mul = Regex::new(
        r"(mul)\(([0-9]{1,3}),([0-9]{1,3})\)|(do)\(\)|(don\'t)\(\)"
    ).unwrap();
    let total: u64 = re_mul.captures_iter(program).scan(true, |enabled, cap| {
        if cap.get(1).is_some() {
            if *enabled {
                return Some(&cap[2].parse::<u64>().unwrap() * &cap[3].parse::<u64>().unwrap())
            }
        } else if cap.get(4).is_some() {
            *enabled = true;
        } else if cap.get(5).is_some() {
            *enabled = false;
        } else {
            panic!("unknown instruction")
        }
        Some(0)
    }).sum();
    println!("{total}");
}

fn main() {
    for arg in env::args().skip(1) {
        println!("=== {arg}");
        let data = read_input(Path::new(&arg)).expect("reading input");
        solve(&data);
    }
}
