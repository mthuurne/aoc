use itertools::Itertools;
use std::{collections::{HashMap, HashSet}, env, fs::File, io::{self, BufRead}, path::Path};

fn read_input(path: &Path) -> io::Result<(usize, usize, HashMap<char, HashSet<(usize, usize)>>)> {
    let file = File::open(path)?;

    let mut antennas = HashMap::new();
    let mut height = 0usize;
    let mut width = 0;
    for (y, line) in io::BufReader::new(file).lines().enumerate() {
        let text = line?;
        height += 1;
        width = text.len();
        for (x, ch) in text.chars().enumerate() {
            if ch != '.' {
                antennas.entry(ch).or_insert_with(|| HashSet::new()).insert((x, y));
            }
        }
    }

    Ok((width, height, antennas))
}


fn solve(width: usize, height: usize, antennas: HashMap<char, HashSet<(usize, usize)>>) {
    let mut antinodes = HashSet::new();

    let mut add_antinodes = |mut x: isize, mut y: isize, dx: isize, dy: isize| {
        while 0 <= x && x < width as isize && 0 <= y && y < height as isize {
            antinodes.insert((x, y));
            x += dx;
            y += dy;
        }
    };

    for locations in antennas.values() {
        for combo in locations.iter().combinations(2) {
            let (x1, y1) = combo[0];
            let (x2, y2) = combo[1];
            let dx = *x2 as isize - *x1 as isize;
            let dy = *y2 as isize - *y1 as isize;
            add_antinodes(*x1 as isize, *y1 as isize, -dx, -dy);
            add_antinodes(*x2 as isize, *y2 as isize, dx, dy);
        }
    }

    println!("{}", antinodes.len());
}

fn main() {
    for arg in env::args().skip(1) {
        println!("=== {arg}");
        let (width, height, antennas) = read_input(Path::new(&arg)).expect("reading input");
        solve(width, height, antennas);
    }
}
