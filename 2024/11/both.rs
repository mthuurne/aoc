use memoize::memoize;
use std::{env, fs::File, io::{self, BufRead}, path::Path};

fn read_input(path: &Path) -> io::Result<Vec<u64>> {
    let file = File::open(path)?;

    let mut stones = Vec::new();
    for line in io::BufReader::new(file).lines() {
        for s in line?.split_whitespace() {
            stones.push(s.parse().expect("number"));
        }
    }

    Ok(stones)
}

#[memoize]
fn simulate(stone: u64, ticks: u32) -> u64 {
    if ticks == 0 {
        1
    } else if stone == 0 {
        simulate(1, ticks - 1)
    } else {
        let mut digits = 0;
        let mut value = stone;
        while value > 0 {
            value /= 10;
            digits += 1;
        }
        if digits & 1 == 0 {
            let split = 10u64.pow(digits >> 1);
            simulate(stone / split, ticks - 1) + simulate(stone % split, ticks - 1)
        } else {
            simulate(stone * 2024, ticks - 1)
        }
    }
}

fn solve(stones: Vec<u64>) {
    println!("after 25 blinks: {}", stones.iter().map(|&stone| simulate(stone, 25)).sum::<u64>());
    println!("after 75 blinks: {}", stones.iter().map(|&stone| simulate(stone, 75)).sum::<u64>());
}

fn main() {
    for arg in env::args().skip(1) {
        println!("=== {arg}");
        let stones = read_input(Path::new(&arg)).expect("reading input");
        solve(stones);
    }
}
