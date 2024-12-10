use std::{collections::HashSet, env, fs::File, io::{self, BufRead}, path::Path};
use itertools::Itertools;

fn read_input(path: &Path) -> io::Result<Vec<Vec<u32>>> {
    let file = File::open(path)?;

    let mut elevations = Vec::new();
    for line in io::BufReader::new(file).lines() {
        let row = line?.chars().map(|ch| ch.to_digit(10).ok_or("digit")).try_collect();
        elevations.push(row.expect("digits"));
    }

    Ok(elevations)
}

type Coord = (usize, usize);

struct Explorer<'a> {
    elevations: &'a Vec<Vec<u32>>,
    todo: Vec<Coord>,
}

impl<'a> Explorer<'a> {
    fn start(elevations: &'a Vec<Vec<u32>>, pos: Coord) -> Self {
        Explorer { elevations: elevations, todo: vec![pos] }
    }
}

fn for_neighbours(pos: Coord, size: Coord, mut f: impl FnMut(Coord)) {
    if pos.0 > 0 { f((pos.0 - 1, pos.1)); }
    if pos.1 > 0 { f((pos.0, pos.1 - 1)); }
    if pos.0 + 1 < size.0 { f((pos.0 + 1, pos.1)); }
    if pos.1 + 1 < size.1 { f((pos.0, pos.1 + 1)); }
}

impl<'a> Iterator for Explorer<'a> {
    type Item = Coord;

    fn next(&mut self) -> Option<Self::Item> {
        let size = (self.elevations[0].len(), self.elevations.len());
        loop {
            match self.todo.pop() {
                Some(pos) => {
                    let elevation = self.elevations[pos.1][pos.0];
                    if elevation == 9 {
                        return Some(pos)
                    } else {
                        for_neighbours(pos, size, |npos| {
                            if self.elevations[npos.1][npos.0] == elevation + 1 {
                                self.todo.push(npos);
                            }
                        });
                    }
                }
                None => return None
            }
        }
    }
}

fn explore(elevations: &Vec<Vec<u32>>, mut f: impl FnMut(Explorer)) {
    let size = (elevations[0].len(), elevations.len());
    for y in 0..size.1 {
        for x in 0..size.0 {
            if elevations[y][x] ==  0 {
                f(Explorer::start(&elevations, (x, y)));
            }
        }
    }
}

fn count_summits(elevations: &Vec<Vec<u32>>, mut f: impl FnMut(Explorer) -> usize) -> usize {
    let mut count = 0;
    explore(elevations, |summits| count += f(summits));
    count
}

fn solve(elevations: Vec<Vec<u32>>) {
    let unique_count = count_summits(&elevations, |summits|
        summits.collect::<HashSet<_>>().len()
    );
    println!("part 1: {unique_count}");

    let path_count = count_summits(&elevations, |summits|
        summits.count()
    );
    println!("part 2: {path_count}");
}

fn main() {
    for arg in env::args().skip(1) {
        println!("=== {arg}");
        let grid = read_input(Path::new(&arg)).expect("reading input");
        solve(grid);
    }
}
